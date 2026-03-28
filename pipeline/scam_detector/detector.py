import json
from .executor import execute_translation, execute_classification
from .builder import build_dynamic_prompt
from .parser import parse_llm_json
from utils import log_scan_result # Import our new logger

def process_message(raw_message: str) -> str:
    """Orchestrates the entire scam detection pipeline."""
    print(f"\n[SYSTEM LOG] 🌐 Original Message: '{raw_message}'")
    
    # 1. Translate
    english_message = execute_translation(raw_message)
    if english_message.lower() != raw_message.lower():
        print(f"[SYSTEM LOG] 🌐 Translated to English: '{english_message}'")
        
    # 2. Build Prompt
    final_prompt = build_dynamic_prompt(english_message)
    
    # 3. Execute Analysis
    raw_response = execute_classification(final_prompt)
    
    # 4. Parse JSON
    final_json_string = parse_llm_json(raw_response)
    
    # 5. Log the result for analytics silently
    try:
        result_dict = json.loads(final_json_string)
        log_scan_result(raw_message, result_dict)
    except Exception as e:
        print(f"[SYSTEM LOG] Failed to log analytics: {e}")
        
    return final_json_string