import os
import json
import pandas as pd
from google import genai
from google.genai import types
from dotenv import load_dotenv
from models import ScamAnalysisResult

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# --- NEW: Dynamic Few-Shot Learning Loop ---
def get_dynamic_examples() -> str:
    """Reads user feedback from the database and formats it as dynamic few-shot examples."""
    examples_text = ""
    # Look for the feedback file in the data folder
    filepath = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "user_feedback.csv")
    
    if os.path.exists(filepath):
        try:
            df = pd.read_csv(filepath)
            # Take the latest 3 pieces of user feedback to train the model dynamically
            latest_feedback = df.tail(3)
            
            if not latest_feedback.empty:
                examples_text += "\n\nCRITICAL CONTEXT FROM PREVIOUS USER CORRECTIONS (Learn from these):\n"
                for index, row in latest_feedback.iterrows():
                    examples_text += f"- Message: '{row['message_text']}'\n"
                    examples_text += f"  * Correct Classification MUST be: {row['user_corrected_label']}\n"
                    examples_text += f"  * User Note/Reasoning: {row['user_comments']}\n"
                examples_text += "\nApply these corrections if you see similar patterns in the new message.\n"
        except Exception as e:
            print(f"[SYSTEM LOG] Error loading dynamic examples: {e}")
            
    return examples_text

# --- Translation Agent ---
def translate_to_english(message_text: str) -> str:
    """Agent responsible for translating any non-English text to English."""
    prompt = f"""
    You are a highly accurate translation API. 
    Detect the language of the following text. If it is already in English, output the exact same text.
    If it is in any other language (e.g., Hindi, Spanish, Hinglish), translate it smoothly into English.
    
    Output ONLY the English text. Do not include notes, language detection labels, or conversational filler.
    
    Text to translate: "{message_text}"
    """
    
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
        config=types.GenerateContentConfig(temperature=0.0) 
    )
    
    return response.text.strip()

# --- External Tool ---
def check_url_in_threat_db(url: str) -> str:
    """Checks if a URL exists in the known scam database. Returns the status."""
    print(f"\n[SYSTEM LOG] 🔍 AI triggered external tool: Checking URL '{url}' against Threat Database...")
    
    known_malicious_domains = ["bit.ly/update-kyc", "bit.ly/fake-update", "free-money-now.com", "hdfc-kyc-update.net"]
    
    if any(domain in url for domain in known_malicious_domains):
        return f"DANGER: The URL {url} is verified as a known phishing/scam link in the threat database."
    
    return f"SAFE: The URL {url} was not found in the threat database (but could still be suspicious based on context)."

# --- Main Classifier Agent ---
def analyze_message_with_llm(raw_message_text: str) -> str:
    print(f"\n[SYSTEM LOG] 🌐 Original Message: '{raw_message_text}'")
    
    # 1. Pass the message through the Translation Agent first
    message_text = translate_to_english(raw_message_text)
    
    if message_text.lower() != raw_message_text.lower():
        print(f"[SYSTEM LOG] 🌐 Translated to English: '{message_text}'")

    # 2. Fetch the latest user feedback to make the AI smarter over time
    dynamic_feedback = get_dynamic_examples()

    # 3. Proceed with the main classification
    prompt = f"""
    You are an expert fraud detection AI. Analyze the text message provided at the end.
    Determine if it is a scam, identify the scam type, extract the manipulative intent, 
    provide step-by-step reasoning, and assign a risk score from 1 to 10.
    
    IMPORTANT INSTRUCTION 1 (TOOLS): 
    If the message contains a URL or link, you MUST use the `check_url_in_threat_db` tool to verify if it is safe before making your final classification. 
    
    IMPORTANT INSTRUCTION 2 (OUTPUT FORMAT):
    Your final response MUST be exactly a raw JSON object matching this schema. Do not include any other text or markdown formatting.
    {ScamAnalysisResult.model_json_schema()}
    
    {dynamic_feedback}

    Message to analyze: "{message_text}"
    """
    
    chat = client.chats.create(
        model='gemini-2.5-flash',
        config=types.GenerateContentConfig(
            temperature=0.1,
            tools=[check_url_in_threat_db],
        )
    )
    
    response = chat.send_message(prompt)
    
    raw_text = response.text.strip()
    if raw_text.startswith("```json"):
        raw_text = raw_text[7:-3].strip()
    elif raw_text.startswith("```"):
        raw_text = raw_text[3:-3].strip()
        
    return raw_text

if __name__ == "__main__":
    # Testing a localized Hindi scam message
    test_msg = "प्रिय ग्राहक, आपका HDFC बैंक खाता आज रात निलंबित कर दिया जाएगा। केवाईसी अपडेट करने के लिए लिंक पर क्लिक करें: http://bit.ly/fake-update"
    
    print("Sending message to ScamGuard AI pipeline...")
    result = analyze_message_with_llm(test_msg)
    print("\nFinal LLM JSON Output:\n", result)