def parse_llm_json(raw_text: str) -> str:
    """Cleans up markdown code blocks from the LLM output to return pure JSON."""
    cleaned_text = raw_text.strip()
    if cleaned_text.startswith("```json"):
        cleaned_text = cleaned_text[7:-3].strip()
    elif cleaned_text.startswith("```"):
        cleaned_text = cleaned_text[3:-3].strip()
    return cleaned_text