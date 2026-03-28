from google.genai import types
from llm.client import client
from llm.prompts import TRANSLATION_PROMPT
from utils import check_url_in_threat_db

def execute_translation(raw_message: str) -> str:
    """Executes the translation agent."""
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=TRANSLATION_PROMPT.format(message=raw_message),
        config=types.GenerateContentConfig(temperature=0.0) 
    )
    return response.text.strip()

def execute_classification(prompt: str) -> str:
    """Executes the main classification agent with tool calling."""
    chat = client.chats.create(
        model='gemini-2.5-flash',
        config=types.GenerateContentConfig(
            temperature=0.1,
            tools=[check_url_in_threat_db],
        )
    )
    response = chat.send_message(prompt)
    return response.text