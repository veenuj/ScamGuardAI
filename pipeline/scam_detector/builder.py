import os
import pandas as pd
from config import FEEDBACK_FILE_PATH
from llm.prompts import CLASSIFICATION_PROMPT
from llm.validator import ScamAnalysisResult

def build_dynamic_prompt(message_text: str) -> str:
    """Reads user feedback and builds the final prompt with dynamic few-shot examples."""
    dynamic_feedback = ""
    
    if os.path.exists(FEEDBACK_FILE_PATH):
        try:
            df = pd.read_csv(FEEDBACK_FILE_PATH)
            latest_feedback = df.tail(3)
            if not latest_feedback.empty:
                dynamic_feedback += "\n\nCRITICAL CONTEXT FROM PREVIOUS USER CORRECTIONS (Learn from these):\n"
                for _, row in latest_feedback.iterrows():
                    dynamic_feedback += f"- Message: '{row['message_text']}'\n"
                    dynamic_feedback += f"  * Correct Classification MUST be: {row['user_corrected_label']}\n"
                    dynamic_feedback += f"  * User Note: {row['user_comments']}\n"
        except Exception as e:
            print(f"[SYSTEM LOG] Error loading dynamic examples: {e}")

    return CLASSIFICATION_PROMPT.format(
        schema=ScamAnalysisResult.model_json_schema(),
        dynamic_context=dynamic_feedback,
        message=message_text
    )