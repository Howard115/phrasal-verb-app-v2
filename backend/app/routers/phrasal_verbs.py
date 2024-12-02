from fastapi import APIRouter, HTTPException, Depends
from fastapi_sso.sso.base import OpenID
from sqlalchemy.orm import Session
import random
import json
from typing import List

from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate

from app.models import (
    PhrasalVerbEntry,
    PhrasalVerbsStoryRequest,
    PhrasalVerbStoryResponse,
    UserData,
    FavoriteStory,
    FavoriteStorySet,
)
from app.utils.phrasal_verbs import load_phrasal_verbs
from app.dependencies import get_logged_user
from app.database import get_db
from app.utils.encryption import decrypt_api_key

router = APIRouter(prefix="/phrasal-verbs", tags=["phrasal_verbs"])


@router.get("/random", response_model=PhrasalVerbEntry)
async def get_random_phrasal_verb():
    """
    Get a random phrasal verb.
    """
    phrasal_verbs = load_phrasal_verbs()

    if not phrasal_verbs:
        raise HTTPException(status_code=404, detail="No phrasal verbs available")

    return random.choice(phrasal_verbs)


@router.post("/generate-story", response_model=PhrasalVerbStoryResponse)
async def generate_story_with_phrasal_verbs(
    request: PhrasalVerbsStoryRequest,
    user: OpenID = Depends(get_logged_user),
    db: Session = Depends(get_db),
):
    """
    Generate a story using the provided phrasal verb entries.
    Requires the user to have a stored OpenAI API key.
    """
    # Fetch user's API key
    db_user = db.query(UserData).filter(UserData.email == user.email).first()
    if not db_user or not db_user.api_key:
        raise HTTPException(
            status_code=400,
            detail="No API key found. Please store your OpenAI API key first.",
        )

    # Decrypt the API key
    try:
        openai_api_key = decrypt_api_key(db_user.api_key)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid API key")

    # Create LLM chain
    llm = ChatOpenAI(
        openai_api_key=openai_api_key, 
        model="gpt-4o", 
        temperature=0.3
    )

    # Prepare phrasal verb details
    phrasal_verb_details = "\n".join([
        f"Phrasal Verb: {pv.phrasal_verb}\n"
        f"Meaning: {pv.meaning}\n"
        f"Example: {pv.example}"
        for pv in request.phrasal_verbs
    ])

    # Prompt template
    prompt = PromptTemplate(
        input_variables=["phrasal_verb_details"],
        template="""
        Create a persuasive mini-argument with an unexpected twist using these phrasal verbs:
        
        {phrasal_verb_details}

        Argument Requirements:
        1. Begin with a serious academic claim
        2. Present a logical cause-and-effect chain
        3. Insert one surprising or humorous twist in the middle
        4. End with a witty or memorable conclusion that ties back to the twist
        5. Keep it under 50 words
        6. Format each phrasal verb in **bold**
        
        Example:
        "Research shows meditation **calms down** workplace stress. When companies **brought in** mindfulness programs, productivity **went up** 30%. Ironically, employees **zoned out** so peacefully, they **missed out** on fire alarms. Perhaps being too zen has its downsides."
        """
    )

    # Create chain
    chain = prompt | llm

    # Generate story
    try:
        # Extract the content from the AIMessage
        result = chain.invoke({"phrasal_verb_details": phrasal_verb_details}).content
        return PhrasalVerbStoryResponse(story=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating story: {str(e)}")


@router.post("/favorites")
async def save_favorite_story(
    favorite: FavoriteStorySet,
    user: OpenID = Depends(get_logged_user),
    db: Session = Depends(get_db),
):
    """Save a favorite phrasal verb story for the logged-in user."""
    # Convert phrasal verbs to JSON string for storage
    phrasal_verbs_json = json.dumps([pv.model_dump() for pv in favorite.phrasal_verbs])
    
    # Create new favorite story
    db_favorite = FavoriteStory(
        email=user.email,
        story=favorite.story,
        phrasal_verbs=phrasal_verbs_json
    )
    
    db.add(db_favorite)
    db.commit()
    db.refresh(db_favorite)
    
    return "Story saved successfully"


@router.get("/favorites", response_model=List[FavoriteStorySet])
async def get_favorite_stories(
    user: OpenID = Depends(get_logged_user),
    db: Session = Depends(get_db),
):
    """Get all favorite stories for the logged-in user."""
    favorites = db.query(FavoriteStory).filter(FavoriteStory.email == user.email).all()
    
    result = []
    for fav in favorites:
        phrasal_verbs = [
            PhrasalVerbEntry(**pv) 
            for pv in json.loads(fav.phrasal_verbs)
        ]
        result.append(FavoriteStorySet(
            id=fav.id,
            story=fav.story,
            phrasal_verbs=phrasal_verbs,
            created_at=fav.created_at
        ))
    
    return result


@router.delete("/favorites/{favorite_id}")
async def delete_favorite_story(
    favorite_id: int,
    user: OpenID = Depends(get_logged_user),
    db: Session = Depends(get_db),
):
    """Delete a favorite story by ID."""
    favorite = db.query(FavoriteStory).filter(
        FavoriteStory.id == favorite_id,
        FavoriteStory.email == user.email
    ).first()
    
    if not favorite:
        raise HTTPException(status_code=404, detail="Favorite story not found")
    
    db.delete(favorite)
    db.commit()
    
    return "Favorite story deleted successfully"
