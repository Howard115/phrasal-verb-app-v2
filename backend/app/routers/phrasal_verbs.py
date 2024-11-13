from fastapi import APIRouter, HTTPException, Depends
from fastapi_sso.sso.base import OpenID
from sqlalchemy.orm import Session
import random

from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate

from app.models import (
    PhrasalVerbEntry,
    PhrasalVerbsStoryRequest,
    PhrasalVerbStoryResponse,
    UserData,
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
        temperature=0.7
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
        Write a concise and engaging short story in exactly 100 words that naturally 
        incorporates the following phrasal verbs:

        {phrasal_verb_details}

        Story Guidelines:
        - Use each phrasal verb at least once
        - Ensure the story demonstrates the meaning of each phrasal verb
        - Make the story coherent and interesting
        - Strictly limit the story to 50 words
        - Use logical descriptions
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
