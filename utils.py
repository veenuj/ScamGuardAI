import os
import pandas as pd
from datetime import datetime
from config import FEEDBACK_FILE_PATH

def check_url_in_threat_db(url: str) -> str:
    """Checks if a URL exists in the known scam database. Returns the status."""
    print(f"\n[SYSTEM LOG] 🔍 AI triggered external tool: Checking URL '{url}' against Threat Database...")
    known_malicious_domains = ["bit.ly/update-kyc", "bit.ly/fake-update", "free-money-now.com", "hdfc-kyc-update.net"]
    
    if any(domain in url for domain in known_malicious_domains):
        return f"DANGER: The URL {url} is verified as a known phishing/scam link in the threat database."
    return f"SAFE: The URL {url} was not found in the threat database."

def save_feedback(original_text: str, ai_classification: str, correct_classification: str, comments: str = ""):
    """Saves incorrect classifications to a CSV for future model training."""
    os.makedirs(os.path.dirname(FEEDBACK_FILE_PATH), exist_ok=True)
    
    new_data = {
        "timestamp": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
        "message_text": [original_text],
        "ai_predicted_label": [ai_classification],
        "user_corrected_label": [correct_classification],
        "user_comments": [comments]
    }
    df_new = pd.DataFrame(new_data)
    
    if os.path.exists(FEEDBACK_FILE_PATH):
        df_new.to_csv(FEEDBACK_FILE_PATH, mode='a', header=False, index=False)
    else:
        df_new.to_csv(FEEDBACK_FILE_PATH, mode='w', header=True, index=False)

# Add this at the very bottom of utils.py
from config import HISTORY_FILE_PATH

def log_scan_result(message: str, result_dict: dict):
    """Logs every processed message and its AI verdict to a CSV for analytics."""
    os.makedirs(os.path.dirname(HISTORY_FILE_PATH), exist_ok=True)
    
    new_data = {
        "timestamp": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
        "message": [message],
        "classification": [result_dict.get("classification", "Unknown")],
        "risk_score": [result_dict.get("risk_score", 0)],
        "scam_type": [result_dict.get("scam_type", "Unknown")]
    }
    df = pd.DataFrame(new_data)
    
    if os.path.exists(HISTORY_FILE_PATH):
        df.to_csv(HISTORY_FILE_PATH, mode='a', header=False, index=False)
    else:
        df.to_csv(HISTORY_FILE_PATH, mode='w', header=True, index=False)