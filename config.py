import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
FEEDBACK_FILE_PATH = os.path.join(os.path.dirname(__file__), "data", "user_feedback.csv")

# Make sure this exact line is at the bottom!
HISTORY_FILE_PATH = os.path.join(os.path.dirname(__file__), "data", "scan_history.csv")