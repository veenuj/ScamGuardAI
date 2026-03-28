import os

# Get the absolute path to the prompts directory
PROMPTS_DIR = os.path.join(os.path.dirname(__file__), "prompts")

def load_prompt(filename: str) -> str:
    """Reads a prompt template from the prompts folder."""
    filepath = os.path.join(PROMPTS_DIR, filename)
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()

# Load the prompts into memory when the app starts
TRANSLATION_PROMPT = load_prompt("translation.txt")
CLASSIFICATION_PROMPT = load_prompt("classification.txt")