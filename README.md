<div align="center">

# 🛡️ ScamGuard AI
**Enterprise-Grade Multi-Agent Fraud Detection System**

[![Python 3.12+](https://img.shields.io/badge/Python-3.12%2B-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.32%2B-FF4B4B?style=for-the-badge&logo=streamlit)](https://streamlit.io/)
[![Google Gemini](https://img.shields.io/badge/Google_GenAI-Gemini_2.5_Flash-8E75B2?style=for-the-badge&logo=google)](https://ai.google.dev/)
[![Pydantic](https://img.shields.io/badge/Pydantic-Structured_Output-E92063?style=for-the-badge)](https://docs.pydantic.dev/)

An advanced Generative AI pipeline designed to dismantle text-based social engineering, phishing, and scam communications in real-time. Built to handle complex, multi-lingual threats using **Tool-Calling (ReAct)**, **Chain-of-Thought (CoT) reasoning**, and **Dynamic Human-in-the-Loop (HITL) learning**.

[Live Demo / Video](#) • [System Architecture](#-system-architecture) • [Installation](#-installation--setup) • [Tech Stack](#-tech-stack) 

</div>

---

## 🛑 The Problem
Traditional keyword-based spam filters are easily bypassed by modern social engineering tactics. Scammers use highly contextual, emotionally charged language (urgency, fear, reward manipulation) and localize their attacks (e.g., Hindi or Hinglish) to evade detection. Static rules cannot reason through psychological manipulation.

## 💡 The Solution
ScamGuard AI abandons static rules in favor of a **Sequential Multi-Agent LLM Pipeline**. It actively reasons through text, translates global threats, autonomously verifies malicious links against external databases, and returns deterministic, structured JSON data for enterprise backend integration.

---

## 🧠 System Architecture

The core engine is built on Google's Gemini 2.5 Flash model, orchestrated into specific agentic roles:

1. **🌐 The Translation Agent:** Intercepts the raw message, detects the language, and normalizes non-English text (e.g., Hindi, Spanish) to English to prevent regional filter bypasses.
2. **🔗 The Tools Engine (ReAct):** The LLM is equipped with a Python tool (`check_url_in_threat_db`). If a URL is detected, the AI pauses its generation, executes the Python function to query the threat database, and injects the result back into its context window.
3. **🕵️ The Classifier Agent:** Consumes the translated text, the tool results, and historical user feedback to generate a final verdict using Few-Shot Prompting and Chain-of-Thought logic.
4. **🔄 Human-in-the-Loop (Dynamic Few-Shot):** User corrections from the UI are saved to a local database (`user_feedback.csv`). The AI dynamically reads this file and injects recent corrections into its system prompt, actively learning from its mistakes (Zero-Day threat adaptation).

---

## 📊 Structured Output (Pydantic)

To ensure backend reliability, the AI is constrained by **Pydantic**. It is mathematically forced to return a strict JSON schema, completely eliminating LLM hallucinations and conversational filler.

**Example Output:**
```json
{
  "classification": "Scam",
  "risk_score": 9,
  "scam_type": "Phishing",
  "manipulative_intent": "Creating false urgency regarding account suspension to steal PAN card credentials.",
  "chain_of_thought_reasoning": "1. The message creates immediate panic by threatening a 24hr account block. 2. It demands sensitive KYC updates via an unofficial link. 3. The ReAct tool confirmed 'bit.ly/fake-update' is a known malicious domain."
}
```
## 💻 Premium User Interface
The frontend is built with Streamlit, customized with CSS to resemble a premium enterprise SaaS dashboard.

* **Sidebar Arsenal:** Quick-test samples, engine capabilities, and developer profile.
* **Component-Based Layouts:** Side-by-side metric columns, dynamic risk-score progress bars, and expandable intelligence reports.
* **Interactive Feedback:** Modern popover menus and toast notifications for the continuous learning loop.

---

## 🛠️ Installation & Setup

**1. Clone the repository**
```bash
git clone [https://github.com/veenuj/ScamGuardAI.git](https://github.com/veenuj/ScamGuardAI.git)
cd ScamGuardAI
```
**2. Create and activate a virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```
**3. Install dependencies**
```bash
pip install -r requirements.txt
```
## 4. Configure Environment##
Create a .env file in the root directory and add your Google Gemini API key:
```bash
GEMINI_API_KEY=your_actual_api_key_here
```
## 5. Launch the application##
```bash
streamlit run app.py
```
## 🏗️ Tech Stack

* **Core AI Engine:** Google GenAI SDK (`gemini-2.5-flash`)
* **Framework:** Python 3.12+
* **Frontend:** Streamlit
* **Data Validation:** Pydantic
* **Data Manipulation:** Pandas (for feedback loop processing)
* **Environment Management:** python-dotenv

---

## 🚀 Future Roadmap

- [ ] **Vector Database Integration:** Replace the CSV feedback loop with Pinecone/ChromaDB for semantic similarity matching on past scams.
- [ ] **WhatsApp API Hook:** Deploy the backend as a FastAPI endpoint to directly intercept and reply to WhatsApp forwards.
- [ ] **Live Threat APIs:** Connect the URL tool directly to Google Safe Browsing or PhishTank APIs for real-time global threat intelligence.

---

## 👨‍💻 Developed By

**Anuj Dhiman** | *Full Stack Developer | GenAI & Multi-Agent Systems Engineer*

Developed as a capstone exploration into advanced Generative AI orchestration, bridging the gap between robust enterprise backend systems and modern LLM capabilities.

---

<div align="center">
  <small>Built with ❤️ using Python, Streamlit, and Google Gemini.</small>
</div>