from pydantic import BaseModel, Field
from typing import Literal

class ScamAnalysisResult(BaseModel):
    classification: Literal["Scam", "Not Scam", "Uncertain"] = Field(description="The final verdict on the message.")
    risk_score: int = Field(description="A risk score from 1 to 10.", ge=1, le=10)
    scam_type: Literal[
        "OTP Fraud", "Phishing", "Account Suspension", 
        "Reward Manipulation", "Fear Tactics", "Fake Authority", 
        "Loan Scams", "Urgency", "None"
    ] = Field(description="The specific category of the scam.")
    manipulative_intent: str = Field(description="A short explanation of the psychological tactic used.")
    chain_of_thought_reasoning: str = Field(description="Step-by-step reasoning explaining why this classification was chosen.")