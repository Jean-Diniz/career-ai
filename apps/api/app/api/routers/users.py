from fastapi import APIRouter, Depends, status, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from app.schemas.user import User, UserCreate, UserWithRelationships
from app.db.crud import get_user, create_user, create_diagnostic, create_study_trail, get_study_trails_by_user
from app.api.deps import get_db, get_current_active_user, get_current_active_user_with_relationships
from app.db.models import User as UserTable
from app.schemas.study_trail import StudyTrailCreate, StudyTrail
import httpx 
import json
from datetime import datetime, timezone
from app.core.config import settings
from python_a2a import A2AClient, ContentType, MessageRole, TextContent, Message
from pydantic import BaseModel

router = APIRouter()

class StudyTrailRequest(BaseModel):
    user_id: int
    linkedin_analysis: str

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
        "parameters": {"max_tokens": 1000, "temperature": 0.7},
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
        linkedin_analysis = resp.json()["response"]
        create_diagnostic(db, linkedin_analysis, linkedin_url, user_id)
                
        resp.raise_for_status()
    except Exception as e:
        print(f"[Background] erro ao chamar Ollama: {e}")

def enqueue_career_path_analysis(db: Session, linkedin_analysis: str, user_id: int) -> None:
    """
    Função para executar análise de carreira em background.
    Usa a mesma abordagem que funciona no test_integration_a2a.py.
    """
    try:
        import asyncio

        # Executar a comunicação A2A
        async def _executar_analise():
            client = A2AClient(settings.a2a_address)

            message_obj = Message(
                content=TextContent(text="Gere uma trilha de estudos: " + linkedin_analysis),
                role=MessageRole.USER
            )

            response = await client.send_message_async(message_obj)

            study_trail = StudyTrailCreate(
                title="Trilha de Estudos Personalizada",
                description="Trilha gerada automaticamente baseada na análise do LinkedIn",
                content=response.content.text,
                user_id=user_id
            )

            create_study_trail(db, study_trail)
            return True
            
        # Criar novo event loop (igual ao test_integration_a2a.py)
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            resultado = loop.run_until_complete(_executar_analise())
            print(f"[Background] Trilha de estudos criada com sucesso para usuário {user_id}")
        finally:
            loop.close()
            
    except Exception as e:
        print(f"[Background] erro ao disparar agente career-path: {e}")
        # Não fazer raise aqui pois é background task

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
    "/users/me/full/", response_model=UserWithRelationships
)
async def read_users_me_full(current_user: UserTable = Depends(get_current_active_user_with_relationships)):
    """
    Retorna o usuário atual com todos os relacionamentos (diagnósticos e trilhas de estudo).
    """
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

@router.post(
    "/users/me/study-trails/"
)
async def create_study_trail_endpoint(
    background_tasks: BackgroundTasks,
    current_user: UserTable = Depends(get_current_active_user_with_relationships),
    db: Session = Depends(get_db)
):
    """
    Cria uma nova trilha de estudos baseada no diagnóstico mais recente do usuário.
    """
    # Verificar se o usuário tem diagnósticos
    if not current_user.diagnostics:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuário não possui diagnósticos. Faça o cadastro primeiro."
        )
    
    # Pegar o diagnóstico mais recente
    latest_diagnostic = current_user.diagnostics[-1]
    
    # Chamar a função como background task
    background_tasks.add_task(
        enqueue_career_path_analysis,
        db,
        latest_diagnostic.diagnostic,
        current_user.id
    )
    
    return {"status": "success", "message": "Trilha de estudos sendo criada em background"}
    