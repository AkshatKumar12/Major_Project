import os
from litellm import acompletion
from src.config import WORKER_MODEL as model_name
from src.config import max_tok

async def analyze_impact(content: str) -> str:
    """
    Evaluates societal, economic, and political impact using LiteLLM.
    """
    
    prompt = (
        "You are a policy and impact analyst. Analyze the following news content and assess "
        "its immediate impact and long-term implications (economic, social, regulatory, or political).\n"
        "Provide a structured 2-paragraph analysis highlighting who is most affected and potential future outcomes.\n\n"
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
        print(f"Error in impact analysis: {e}")
        return "Error analyzing impact."