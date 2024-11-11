from fastapi import APIRouter, HTTPException
import random

from app.models import PhrasalVerbEntry
from app.utils.phrasal_verbs import load_phrasal_verbs

router = APIRouter(
    prefix="/phrasal-verbs",
    tags=["phrasal_verbs"]
)

@router.get("/random", response_model=PhrasalVerbEntry)
async def get_random_phrasal_verb():
    """
    Get a random phrasal verb.
    """
    phrasal_verbs = load_phrasal_verbs()
    
    if not phrasal_verbs:
        raise HTTPException(
            status_code=404, 
            detail="No phrasal verbs available"
        )
    
    return random.choice(phrasal_verbs) 