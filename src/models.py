from pydantic import BaseModel, Field
from typing import Literal

class ScamAnalysisResult(BaseModel):
    # Enforcing strict categories as defined in the problem statement
    classification: Literal["Scam", "Not Scam", "Uncertain"] = Field(
        description="The final verdict on the message."
    )
    
    # --- NEW: Risk Scoring Requirement ---
    risk_score: int = Field(
        description="A risk score from 1 to 10, where 1 is completely safe and 10 is a severe, confirmed threat.",
        ge=1, le=10 # 'ge' means greater than or equal to, 'le' means less than or equal to
    )
    
    scam_type: Literal[
        "OTP Fraud", "Phishing", "Account Suspension", 
        "Reward Manipulation", "Fear Tactics", "Fake Authority", 
        "Loan Scams", "Urgency", "None"
    ] = Field(
        description="The specific category of the scam. If Not Scam, output 'None'."
    )
    
    manipulative_intent: str = Field(
        description="A short explanation of the psychological tactic used (e.g., 'Creating false time pressure')."
    )
    
    chain_of_thought_reasoning: str = Field(
        description="Step-by-step reasoning explaining why this classification was chosen."
    )