import streamlit as st
import json
import sys
import os
import pandas as pd
from datetime import datetime

# Link the src folder so we can import our AI backend
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
from llm_analyzer import analyze_message_with_llm

# --- Function: Save User Feedback ---
def save_feedback(original_text, ai_classification, correct_classification, comments=""):
    """Saves incorrect classifications to a CSV for future model training."""
    os.makedirs("data", exist_ok=True)
    filepath = "data/user_feedback.csv"
    
    new_data = {
        "timestamp": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
        "message_text": [original_text],
        "ai_predicted_label": [ai_classification],
        "user_corrected_label": [correct_classification],
        "user_comments": [comments]
    }
    df_new = pd.DataFrame(new_data)
    
    if os.path.exists(filepath):
        df_new.to_csv(filepath, mode='a', header=False, index=False)
    else:
        df_new.to_csv(filepath, mode='w', header=True, index=False)

# --- Page Configuration ---
st.set_page_config(
    page_title="ScamGuard AI | By Anuj Dhiman", 
    page_icon="🤖", 
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- Custom CSS for Premium UI Polish ---
st.markdown("""
    <style>
    /* Main Background & Text */
    .stTextArea textarea { font-size: 16px !important; border-radius: 10px; border: 1px solid #d1d5db;}
    .main-header { font-size: 2.8rem; font-weight: 800; background: -webkit-linear-gradient(45deg, #1E3A8A, #3B82F6); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 0;}
    .sub-header { font-size: 1.15rem; color: #4B5563; margin-bottom: 2rem; font-weight: 500;}
    
    /* Button Styling */
    .stButton>button { border-radius: 8px; font-weight: 600; transition: all 0.3s ease; }
    .stButton>button:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3); }
    
    /* Footer */
    .footer { position: fixed; bottom: 0; left: 0; width: 100%; background-color: transparent; text-align: center; padding: 10px; font-size: 0.9rem; color: #6B7280; }
    </style>
""", unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    # New Modern AI Security Logo
    st.image("https://cdn-icons-png.flaticon.com/512/8616/8616788.png", width=90) 
    st.title("ScamGuard AI")
    st.caption("v2.0.0 | GenAI Pipeline")
    
    st.divider()
    
    st.markdown("### ⚙️ Engine Capabilities")
    st.markdown("- 🌐 **Auto-Translation** (Hindi, Spanish, etc.)")
    st.markdown("- 🔗 **Live URL Threat Checking**")
    st.markdown("- 🧠 **Zero-Day Scam Detection**")
    st.markdown("- 🕵️ **Manipulative Intent Analysis**")
    
    st.divider()
    
    # Quick Test Arsenal
    with st.expander("🧪 Quick Test Samples"):
        st.markdown("**1. Urgent Phishing (English)**")
        st.code("Urgent: Your Axis Bank KYC is expiring today. Update PAN via http://bit.ly/fake-update to avoid account block.")
        st.markdown("**2. Fear Tactic (Hindi)**")
        st.code("प्रिय ग्राहक, आपका बिजली कनेक्शन रात 9 बजे काट दिया जाएगा। तुरंत 9876543210 पर कॉल करें।")
        st.markdown("**3. Safe Conversation**")
        st.code("Hey! Are we still on for the system architecture review meeting at 4 PM tomorrow?")

    st.divider()
    
    # Developer Profile Showcase
    st.markdown("### 👨‍💻 Developer Profile")
    st.markdown("**Anuj Dhiman**")
    st.caption("Full Stack Developer | GenAI & Multi-Agent Systems Engineer")
    st.markdown("[LinkedIn](https://www.linkedin.com/in/anuj-dhiman3112) | [GitHub](https://github.com/veenuj)")

# --- Main App Header ---
st.markdown('<p class="main-header">🛡️ ScamGuard AI Scanner</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Real-time Multi-Agent Threat Detection for SMS, Email, and WhatsApp.</p>', unsafe_allow_html=True)

# --- Tabs for Clean Organization ---
tab1, tab2 = st.tabs(["🔍 Analyze Message", "📖 Architecture Overview"])

with tab2:
    st.markdown("### 🧠 The Multi-Agent Architecture")
    st.write("This application utilizes an advanced LLM pipeline to dismantle text-based social engineering:")
    st.info("**1. Translation Agent:** Normalizes global threats by converting non-English text (e.g., Hindi) to English.\n\n**2. Tool Calling (ReAct):** Autonomously scans extracted URLs against known malicious databases.\n\n**3. Classifier Agent:** Employs Few-Shot Prompting and Chain-of-Thought reasoning to expose underlying manipulative psychology.")

with tab1:
    # --- Input Section ---
    message_input = st.text_area("Paste suspicious text here:", height=140, placeholder="Copy a message from the 'Quick Test Samples' in the sidebar, or paste your own...")

    # --- Action Button ---
    if st.button("🚀 Analyze Threat Level", type="primary", use_container_width=True):
        if not message_input.strip():
            st.warning("⚠️ Please enter a message to analyze.")
        else:
            with st.spinner("🤖 Agents are translating, scanning URLs, and analyzing psychological intent..."):
                try:
                    # Call the AI Backend
                    raw_result = analyze_message_with_llm(message_input)
                    result = json.loads(raw_result)
                    
                    # --- Results Display ---
                    st.divider()
                    st.markdown("### 📊 Intelligence Report")
                    
                    classification = result.get("classification", "Uncertain")
                    
                    # Hero Banner for Verdict
                    if classification == "Scam":
                        st.error(f"## 🚨 THREAT DETECTED: {classification.upper()}", icon="🚨")
                    elif classification == "Not Scam":
                        st.success(f"## ✅ SAFE: {classification.upper()}", icon="✅")
                    else:
                        st.warning(f"## ⚠️ WARNING: {classification.upper()}", icon="⚠️")
                        
                    # --- NEW: Risk Score Visual ---
                    risk_score = result.get("risk_score", 1)
                    st.markdown(f"**Threat Risk Score: {risk_score}/10**")
                    st.progress(float(risk_score) / 10.0)
                    st.markdown("<br>", unsafe_allow_html=True)
                    
                    # Side-by-side data columns
                    col1, col2 = st.columns(2)
                    with col1:
                        st.info(f"**Primary Tactic:**\n\n{result.get('scam_type', 'N/A')}")
                    with col2:
                        st.warning(f"**Psychological Intent:**\n\n{result.get('manipulative_intent', 'N/A')}")
                    
                    # Expandable reasoning
                    with st.expander("🕵️‍♂️ View AI Step-by-Step Reasoning"):
                        st.write(result.get("chain_of_thought_reasoning", "No reasoning provided."))
                        st.caption("Note: Tool execution logs (like URL database lookups) are recorded in the host terminal.")
                    
                    # --- User Feedback Loop ---
                    st.divider()
                    st.markdown("#### 🧠 Help Train the Model")
                    st.write("Did the AI get this right?")
                    
                    f_col1, f_col2 = st.columns(2)
                    
                    with f_col1:
                        if st.button("👍 Yes, it's accurate", use_container_width=True):
                            st.toast("Feedback logged. Thank you!", icon="✅")
                            
                    with f_col2:
                        with st.popover("👎 No, report error", use_container_width=True):
                            st.write("Help us improve by providing the correct label.")
                            opposite_label = "Not Scam" if classification == "Scam" else "Scam"
                            correct_label = st.selectbox("Correct Verdict:", ["Scam", "Not Scam", "Uncertain"], index=["Scam", "Not Scam", "Uncertain"].index(opposite_label))
                            user_note = st.text_input("Why did the AI fail? (Optional)")
                            
                            if st.button("Submit Correction", type="primary"):
                                save_feedback(message_input, classification, correct_label, user_note)
                                st.toast("Correction saved to database for the next training cycle!", icon="💾")
                                
                except Exception as e:
                    st.error(f"An error occurred during pipeline execution: {e}")

# --- Footer ---
st.markdown('<div class="footer">Built with ❤️ by Anuj Dhiman using Streamlit & Google Gemini</div>', unsafe_allow_html=True)