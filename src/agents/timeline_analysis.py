import os
from litellm import acompletion
from src.config import WORKER_MODEL as model_name
from src.config import max_tok

async def extract_timeline(content: str) -> list[str]:
    """
    Extracts a chronological timeline of events from the text using LiteLLM.
    """
    
    prompt = (
        "You are an investigative journalist. Analyze the following text and construct "
        "a chronological timeline of events mentioned.\n"
        "Format the output strictly as a bulleted list where each item starts with a date/time or time anchor "
        "(e.g., 'YYYY-MM-DD: Event description' or 'Early Morning: Event description').\n\n"
        f"Text:\n{content}"
    )
    
    try:
        response = await acompletion(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tok
        )
        
        raw_text = response.choices[0].message.content
        timeline_items = [
            line.strip().lstrip('-* ') for line in raw_text.split('\n') if line.strip()
        ]
        return timeline_items
    except Exception as e:
        print(f"Error in timeline analysis: {e}")
        return ["Error extracting timeline."]