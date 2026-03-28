import streamlit as st
import pandas as pd
import json
import sys
import os
import time

# Link the root folder so we can import our pipeline modules and config
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from pipeline.scam_detector.detector import process_message
from utils import save_feedback
from config import HISTORY_FILE_PATH

# --- Page Configuration ---
st.set_page_config(
    page_title="ScamGuard AI | Enterprise", 
    page_icon="🛡️", 
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- Ultra Premium CSS with Realistic Animations ---
st.markdown("""
    <style>
    /* Premium Typography */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }

    /* Core Entrance Animation */
    @keyframes smoothFadeInUp {
        0% { opacity: 0; transform: translateY(20px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    .stApp {
        animation: smoothFadeInUp 0.8s cubic-bezier(0.16, 1, 0.3, 1);
    }

    /* Animated Gradient Header */
    .premium-header {
        font-size: 3.2rem;
        font-weight: 800;
        background: linear-gradient(300deg, #2563eb, #7c3aed, #06b6d4, #2563eb);
        background-size: 300% 300%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: gradientFlow 8s ease infinite;
        letter-spacing: -1.5px;
        margin-bottom: 0.2rem;
        line-height: 1.2;
    }
    .premium-subheader {
        font-size: 1.15rem;
        color: #64748b;
        font-weight: 500;
        margin-bottom: 2rem;
    }

    @keyframes gradientFlow {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Realistic Neumorphic/Glass Text Area */
    .stTextArea textarea {
        border-radius: 12px !important;
        border: 1px solid rgba(148, 163, 184, 0.3) !important;
        background-color: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(10px) !important;
        box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.02) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        padding: 1rem !important;
    }
    .stTextArea textarea:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.15), inset 0 2px 4px rgba(0,0,0,0.01) !important;
        transform: translateY(-2px);
    }

    /* Liquid Gradient Primary Button */
    button[kind="primary"] {
        background: linear-gradient(45deg, #1d4ed8, #3b82f6, #6366f1);
        background-size: 200% 200%;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        font-size: 1.05rem !important;
        padding: 0.6rem !important;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
        box-shadow: 0 4px 15px -3px rgba(59, 130, 246, 0.4) !important;
    }
    button[kind="primary"]:hover {
        background-position: 100% 0%;
        transform: translateY(-4px) scale(1.01) !important;
        box-shadow: 0 12px 25px -5px rgba(59, 130, 246, 0.6) !important;
    }

    /* Metric Cards - Magnetic Hover Physics */
    [data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(148, 163, 184, 0.2);
        backdrop-filter: blur(8px);
        border-radius: 16px;
        padding: 1.2rem;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    [data-testid="stMetric"]:hover {
        transform: translateY(-6px) scale(1.02);
        box-shadow: 0 15px 30px -10px rgba(0, 0, 0, 0.1);
        border-color: rgba(59, 130, 246, 0.4);
    }

    /* Threat Pulse Animation */
    @keyframes redPulseGlow {
        0% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.4); }
        70% { box-shadow: 0 0 0 15px rgba(239, 68, 68, 0); }
        100% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0); }
    }
    .threat-alert {
        animation: redPulseGlow 2s infinite;
        border-radius: 8px;
    }

    /* Shield Logo Floating Animation */
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-8px); }
        100% { transform: translateY(0px); }
    }
    .animated-shield {
        font-size: 4rem;
        text-align: center;
        animation: float 4s ease-in-out infinite;
        margin-bottom: 1rem;
    }

    /* Sleek Footer */
    .footer {
        text-align: center;
        padding: 2rem 0 1rem 0;
        color: #94a3b8;
        font-size: 0.85rem;
        font-weight: 500;
        letter-spacing: 0.5px;
    }
    </style>
""", unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    # Reliable, Animated CSS Logo
    st.markdown('<div class="animated-shield">🛡️</div>', unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; margin-top: -10px;'>ScamGuard AI</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #64748b;'>v2.0.0 | Enterprise Engine</p>", unsafe_allow_html=True)
    
    st.divider()
    
    st.markdown("### ⚙️ Capabilities")
    st.markdown("🌐 **Auto-Translation** (Global)")
    st.markdown("🔗 **Live URL Threat Check**")
    st.markdown("🧠 **Zero-Day Detection**")
    st.markdown("🕵️ **Intent Analysis**")
    
    st.divider()
    
    # Quick Test Arsenal
    with st.expander("🧪 Quick Test Samples"):
        st.markdown("**1. Urgent Phishing**")
        st.code("Urgent: Your Axis Bank KYC is expiring today. Update PAN via http://bit.ly/fake-update to avoid account block.")
        st.markdown("**2. Fear Tactic (Hindi)**")
        st.code("प्रिय ग्राहक, आपका बिजली कनेक्शन रात 9 बजे काट दिया जाएगा। तुरंत 9876543210 पर कॉल करें।")
        st.markdown("**3. Safe Conversation**")
        st.code("Hey! Are we still on for the system architecture review meeting at 4 PM tomorrow?")

    st.divider()
    
    # Developer Profile Showcase
    st.markdown("### 👨‍💻 Developer")
    st.markdown("**Anuj Dhiman**")
    st.caption("GenAI & Multi-Agent Systems Engineer")
    st.markdown("[LinkedIn](https://www.linkedin.com/in/anuj-dhiman3112) | [GitHub](https://github.com/veenuj)")

# --- Main App Header ---
st.markdown('<div class="premium-header">ScamGuard AI Scanner</div>', unsafe_allow_html=True)
st.markdown('<div class="premium-subheader">Real-time Multi-Agent Threat Detection for Enterprise.</div>', unsafe_allow_html=True)

# --- Tabs ---
tab1, tab2, tab3 = st.tabs(["🔍 Live Scanner", "📖 Architecture", "📈 Analytics Dashboard"])

with tab2:
    st.markdown("### 🧠 The Multi-Agent Architecture")
    st.write("This application utilizes an advanced LLM pipeline to dismantle text-based social engineering:")
    st.info("**1. Translation Agent:** Normalizes global threats by converting non-English text (e.g., Hindi) to English.\n\n**2. Tool Calling (ReAct):** Autonomously scans extracted URLs against known malicious databases.\n\n**3. Classifier Agent:** Employs Few-Shot Prompting and Chain-of-Thought reasoning to expose underlying manipulative psychology.")

with tab3:
    st.markdown("### 📈 Global Threat Analytics")
    st.write("Live system metrics tracking all processed communications.")
    
    if os.path.exists(HISTORY_FILE_PATH):
        try:
            df_history = pd.read_csv(HISTORY_FILE_PATH)
            
            # Calculate Metrics
            total_scans = len(df_history)
            total_scams = len(df_history[df_history['classification'] == 'Scam'])
            avg_risk = round(df_history['risk_score'].mean(), 1) if not df_history.empty else 0
            
            # Display Top Level Metrics
            m1, m2, m3 = st.columns(3)
            m1.metric("Total Scans", total_scans, delta="Online", delta_color="normal")
            m2.metric("Threats Blocked", total_scams, delta="Protected", delta_color="inverse")
            m3.metric("Avg Risk Score", f"{avg_risk}/10")
            
            st.divider()
            
            # Display Charts
            st.markdown("#### 🎯 Scam Categories Detected")
            threats_only = df_history[df_history['classification'] == 'Scam']
            if not threats_only.empty:
                category_counts = threats_only['scam_type'].value_counts()
                st.bar_chart(category_counts, color="#3b82f6")
            else:
                st.info("No active threats detected yet.")
                
            st.divider()
            
            st.markdown("#### 📜 Recent Scan Logs")
            st.dataframe(df_history.tail(10).iloc[::-1], use_container_width=True)
            
        except Exception as e:
            st.error(f"Error loading analytics data: {e}")
    else:
        st.info("📊 Analytics database is initializing. Scan a message to generate insights.")

with tab1:
    # --- Input Section ---
    message_input = st.text_area("Analyze Communications:", height=150, placeholder="Paste a suspicious SMS, Email, or WhatsApp message here...")

    # --- Action Button ---
    if st.button("🚀 Initiate Deep Scan", type="primary", use_container_width=True):
        if not message_input.strip():
            st.warning("⚠️ Please enter a message to analyze.")
        else:
            # Clean progress bar animation
            progress_text = "Agents translating & verifying databases..."
            my_bar = st.progress(0, text=progress_text)
            for percent_complete in range(100):
                time.sleep(0.01)
                my_bar.progress(percent_complete + 1, text=progress_text)
            my_bar.empty()

            with st.spinner("🧠 Synthesizing psychological intent..."):
                try:
                    # Call the AI Backend
                    raw_result = process_message(message_input)
                    result = json.loads(raw_result)
                    
                    # --- Results Display ---
                    st.divider()
                    st.markdown("### 📊 Intelligence Report")
                    
                    classification = result.get("classification", "Uncertain")
                    
                    # Hero Banner for Verdict with Threat Pulse
                    if classification == "Scam":
                        st.markdown('<div class="threat-alert">', unsafe_allow_html=True)
                        st.error(f"## 🚨 THREAT DETECTED: {classification.upper()}", icon="🚨")
                        st.markdown('</div>', unsafe_allow_html=True)
                    elif classification == "Not Scam":
                        st.success(f"## ✅ SAFE: {classification.upper()}", icon="✅")
                    else:
                        st.warning(f"## ⚠️ WARNING: {classification.upper()}", icon="⚠️")
                        
                    # Risk Score Visual
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
                    
                    # --- User Feedback Loop ---
                    st.divider()
                    st.markdown("#### 🔄 Continuous Learning Loop")
                    st.write("Verify this classification to fine-tune the LLM:")
                    
                    f_col1, f_col2 = st.columns(2)
                    
                    with f_col1:
                        if st.button("👍 Correct Verdict", use_container_width=True):
                            st.toast("System updated. Thank you!", icon="✅")
                            
                    with f_col2:
                        with st.popover("👎 Incorrect Verdict", use_container_width=True):
                            st.write("Help correct the system:")
                            opposite_label = "Not Scam" if classification == "Scam" else "Scam"
                            correct_label = st.selectbox("Correct Status:", ["Scam", "Not Scam", "Uncertain"], index=["Scam", "Not Scam", "Uncertain"].index(opposite_label))
                            user_note = st.text_input("Reasoning (Optional):")
                            
                            if st.button("Submit Patch", type="primary", key="patch_btn"):
                                save_feedback(message_input, classification, correct_label, user_note)
                                st.toast("Patch saved for next training cycle!", icon="💾")
                                
                except Exception as e:
                    st.error(f"An error occurred during pipeline execution: {e}")

# --- Footer ---
st.markdown('<div class="footer">Developed with ❤️ by Anuj Dhiman</div>', unsafe_allow_html=True)