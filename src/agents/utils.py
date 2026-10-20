import re

def clean_llm_output(text: str) -> str:
    """Strips <think> tags, scratchpads, and 'Here's a thinking process' blocks."""
    if not text:
        return ""
    
    # 1. Strip XML/HTML reasoning tags
    text = re.sub(r'<think>[\s\S]*?</think>', '', text, flags=re.IGNORECASE)
    text = re.sub(r'<thought>[\s\S]*?</thought>', '', text, flags=re.IGNORECASE)
    
    # 2. Strip conversational scratchpad headers
    if "Here's a thinking process:" in text:
        # Split off everything before the actual response if marked by double linebreaks
        sections = re.split(r'\n\s*\n', text)
        clean_sections = [
            s for s in sections 
            if not s.strip().lower().startswith("here's a thinking process")
            and not s.strip().lower().startswith("analyze user")
        ]
        text = "\n\n".join(clean_sections)
        
    return text.strip()