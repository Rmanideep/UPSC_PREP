from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
import json

# Load environment variables
load_dotenv()

def get_llm_model(api_key: str = None):
    """Initialize and return the LLM model configured for OpenRouter"""
    # Use provided API key or fall back to environment variable
    openrouter_api_key = api_key or os.getenv("OPENROUTER_API_KEY")
    
    if not openrouter_api_key:
        raise ValueError("OpenRouter API key is required. Please provide it or set OPENROUTER_API_KEY environment variable.")
    
    return ChatOpenAI(
        model="mistralai/mistral-7b-instruct:free",
        temperature=0.7,
        openai_api_key=openrouter_api_key,
        openai_api_base="https://openrouter.ai/api/v1"
    )

def get_structured_response(model, prompt: str) -> dict:
    """Get a structured response from the model"""
    system_prompt = """You are an essay evaluator. Provide feedback and scoring in JSON format.
    Your response should be a valid JSON object with two fields:
    1. feedback: A detailed feedback string
    2. score: An integer score from 0 to 10

    Example response format:
    {
        "feedback": "Your detailed feedback here...",
        "score": 8
    }
    """
    
    response = model.invoke(
        [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
    )
    
    try:
        # Extract the JSON from the response
        result = json.loads(response.content)
        return result
    except json.JSONDecodeError:
        # Fallback if response is not valid JSON
        return {
            "feedback": response.content,
            "score": 5  # Default score
        }
