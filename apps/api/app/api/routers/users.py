from fastapi import APIRouter, Depends, status, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from app.schemas.user import User, UserCreate
from app.db.crud import get_user, create_user, create_diagnostic, create_study_trail, get_study_trails_by_user
from app.api.deps import get_db, get_current_active_user
from app.db.models import User as UserTable
from app.schemas.study_trail import StudyTrailCreate, StudyTrail
import httpx 
import json
from app.core.config import settings
from python_a2a import A2AClient

router = APIRouter()

def enqueue_ollama_analysis(db: Session, linkedin_url: str, user_id: int) -> None:
    prompt = """"
        You are a Professional LinkedIn Profile Analyst. When given only a LinkedIn profile URL, your task is to:

        1. Extract and structure the following information:
        - Full name
        - Current job title and company
        - Location
        - Industry

        2. Summarize the candidate's career in up to three bullet points, highlighting:
        - Key responsibilities and achievements
        - Areas of expertise

        3. List the top five skills displayed on the profile and include the number of endorsements for each.

        4. Report how many recommendations the profile has, and briefly quote up to two representative excerpts.

        5. Evaluate the profile's completeness (photo, headline, summary, experience entries, skills, accomplishments) and assign a score from 0 to 100.

        6. Generate an "Attractiveness Score" from 0 to 10 based on content relevance, clarity, and overall presentation.

        7. Provide three practical improvement suggestions (e.g., refine headline, enhance "About" section, showcase top projects or certifications).

        Return your output as a single JSON object with exactly these keys, return ONLY JSON:

        {
            "linkedin_url": "linkedin_url",
            "name": "...",
            "current_position": "...",
            "location": "...",
            "industry": "...",
            "summary": ["...", "...", "..."],
            "top_skills": [
                { "skill": "...", "endorsements": 0 },
                ...
            ],
            "recommendations_count": 0,
            "highlighted_recommendations": ["...", "..."],
            "profile_completeness": 0,
            "attractiveness_score": 0,
            "improvement_suggestions": ["...", "...", "..."]
        }

        Linkedin Url: 
    """ + linkedin_url

    payload = {
        "model": settings.ollama_model,
        "prompt": prompt,
        "parameters": {"max_tokens": 128, "temperature": 0.7},
        "stream": False
    }

    try:
        print(f"{settings.ollama_address}/api/generate")
        resp = httpx.post(
            f"{settings.ollama_address}/api/generate", 
            json=payload, 
            timeout=int(settings.ollama_timeout)
        )
        
        # Salvar diagnóstico vinculado ao usuário
        create_diagnostic(db, resp.json()["response"], linkedin_url, user_id)
        
        # Após o diagnóstico, chamar o agente career-path
        enqueue_career_path_analysis(db, resp.json()["response"], user_id)

        resp.raise_for_status()
    except Exception as e:
        print(f"[Background] erro ao chamar Ollama: {e}")

def enqueue_career_path_analysis(db: Session, linkedin_analysis: str, user_id: int) -> None:
    """
    Chama o agente career-path para gerar uma trilha de estudos baseada na análise do LinkedIn.
    """
    try:
        # Converter análise do LinkedIn para formato do PerfilPessoa
        profile_data = convert_linkedin_to_profile(linkedin_analysis)
        
        # Conectar ao agente career-path
        client = A2AClient(base_url="http://career-path:5000")
        
        # Chamar o skill de gerar trilha
        response = client.call_skill(
            "Gerar Trilha de Estudos",
            profile_data
        )
        
        # Salvar trilha no banco
        study_trail = StudyTrailCreate(
            title="Trilha de Estudos Personalizada",
            description="Trilha gerada automaticamente baseada na análise do LinkedIn",
            content=response,
            user_id=user_id
        )
        
        create_study_trail(db, study_trail)
        
        print(f"[Background] Trilha de estudos criada para usuário {user_id}")
        
    except Exception as e:
        print(f"[Background] erro ao chamar agente career-path: {e}")

def convert_linkedin_to_profile(linkedin_analysis: str) -> str:
    """
    Converte a análise do LinkedIn para o formato PerfilPessoa esperado pelo agente.
    """
    try:
        # Parse da análise do LinkedIn
        analysis_data = json.loads(linkedin_analysis)
        
        # Criar perfil baseado na análise
        profile = {
            "nome": analysis_data.get("name", "Nome não informado"),
            "escolaridade": "Superior",  # Padrão, pode ser ajustado
            "area_formacao": analysis_data.get("industry", "Não informado"),
            "competencias_atuais": [
                {
                    "area": skill["skill"],
                    "nivel": "intermediário",
                    "experiencia_anos": 2,
                    "detalhes": f"Endorsements: {skill['endorsements']}"
                }
                for skill in analysis_data.get("top_skills", [])[:3]
            ],
            "objetivos_carreira": [
                {
                    "cargo_desejado": "Desenvolvedor Sênior",
                    "area_interesse": analysis_data.get("industry", "Tecnologia"),
                    "prazo_anos": 2,
                    "motivacao": "Crescimento profissional baseado na análise do LinkedIn"
                }
            ],
            "disponibilidade_estudo_horas_semana": 10,
            "preferencia_aprendizado": "online",
            "recursos_disponiveis": "cursos online, livros, certificações"
        }
        
        return json.dumps(profile, ensure_ascii=False, indent=2)
        
    except Exception as e:
        print(f"Erro ao converter análise do LinkedIn: {e}")
        # Retornar perfil padrão em caso de erro
        default_profile = {
            "nome": "Usuário",
            "escolaridade": "Superior",
            "area_formacao": "Tecnologia",
            "competencias_atuais": [
                {
                    "area": "Desenvolvimento",
                    "nivel": "intermediário",
                    "experiencia_anos": 2,
                    "detalhes": "Baseado na análise do LinkedIn"
                }
            ],
            "objetivos_carreira": [
                {
                    "cargo_desejado": "Desenvolvedor Sênior",
                    "area_interesse": "Tecnologia",
                    "prazo_anos": 2,
                    "motivacao": "Crescimento profissional"
                }
            ],
            "disponibilidade_estudo_horas_semana": 10,
            "preferencia_aprendizado": "online",
            "recursos_disponiveis": "cursos online, livros"
        }
        
        return json.dumps(default_profile, ensure_ascii=False, indent=2)

@router.post(
    "/users/", response_model=User, status_code=status.HTTP_201_CREATED
)
def register_user(
    user_in: UserCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    if get_user(db, user_in.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )
    if user_in.email and db.query(UserTable).filter(UserTable.email == user_in.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    
    user = create_user(db, user_in)

    background_tasks.add_task(
        enqueue_ollama_analysis,
        db,
        user.linkedin_url,
        user.id
    )

    return user

@router.get(
    "/users/me/", response_model=User
)
async def read_users_me(current_user = Depends(get_current_active_user)):
    return current_user

@router.get(
    "/users/me/study-trails/", response_model=list[StudyTrail]
)
async def get_my_study_trails(
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Retorna todas as trilhas de estudos do usuário logado.
    """
    return get_study_trails_by_user(db, current_user.id)