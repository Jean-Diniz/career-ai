from fastapi import APIRouter, Depends, status, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from app.schemas.user import User, UserCreate
from app.db.crud import get_user, create_user, create_diagnostic
from app.api.deps import get_db, get_current_active_user
from app.db.models import User as UserTable
import httpx 
from app.core.config import settings

router = APIRouter()

def enqueue_ollama_analysis(db: Session, linkedin_url: str, ) -> None:
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

        6. Generate an “Attractiveness Score” from 0 to 10 based on content relevance, clarity, and overall presentation.

        7. Provide three practical improvement suggestions (e.g., refine headline, enhance “About” section, showcase top projects or certifications).

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
        
        create_diagnostic(db, resp.json()["response"], linkedin_url)

        resp.raise_for_status()
    except Exception as e:
        print(f"[Background] erro ao chamar Ollama: {e}")

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
        user.linkedin_url
    )

    return user

@router.get(
    "/users/me/", response_model=User
)
async def read_users_me(current_user = Depends(get_current_active_user)):
    return current_user