import os
from litellm import acompletion
from src.config import WORKER_MODEL as model_name
from src.config import max_tok

async def analyze_perspective(content: str) -> str:
    """
    Analyzes the bias, tone, and viewpoint of the provided text using LiteLLM.
    """
    
    prompt = (
        "You are an impartial media analyst. Analyze the following text for "
        "ideological bias, tone, and underlying perspective. Provide a concise, "
        "1-2 paragraph summary of the viewpoint presented.\n\n"
        f"Text:\n{content}"
    )
    
    try:
        response = await acompletion(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tok
        )
        
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error in perspective analysis: {e}")
        return "Error analyzing perspective."