import os
from litellm import acompletion
from src.config import WORKER_MODEL as model_name
from src.config import max_tok

async def extract_and_verify_claims(content: str) -> list[str]:
    """
    Extracts key claims from the text using LiteLLM and OpenRouter.
    """
    
    prompt = (
        "You are an expert fact-checker. Extract the key factual claims from "
        "the following text. Return ONLY a bulleted list of the claims, with a "
        "short note on whether each is easily verifiable.\n\n"
        f"Text:\n{content}"
    )
    
    try:
        response = await acompletion(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tok
        )
        
        # Parse the bulleted list into a Python list
        raw_text = response.choices[0].message.content
        claims = [line.strip().lstrip('-* ') for line in raw_text.split('\n') if line.strip()]
        return claims
    except Exception as e:
        print(f"Error in claim verification: {e}")
        return ["Error extracting claims."]