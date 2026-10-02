import streamlit as st
import json
import os
import requests

# Page Configuration
st.set_page_config(
    page_title="StudyBuddy AI - Build for a Friend",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling for clean modern UI
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E88E5;
        margin-bottom: 0px;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #555;
        margin-bottom: 25px;
    }
    .metric-card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 15px;
        border-left: 4px solid #1E88E5;
        margin-bottom: 15px;
    }
    .quiz-card {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 18px;
        margin-bottom: 15px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.04);
    }
</style>
""", unsafe_allow_html=True)

# Sidebar Configuration
with st.sidebar:
    st.image("https://raw.githubusercontent.com/open-telemetry/opentelemetry.io/main/icon.png", width=60)
    st.title("⚙️ Model Settings")
    st.markdown("Powered by **Open-Weight AI Models** (Llama-3 / Mistral) for Hacktoberfest 2026.")
    
    api_provider = st.selectbox(
        "Inference Provider",
        ["Groq (Ultra-fast Open Llama 3)", "Hugging Face Inference API", "Demo / Offline Mode"]
    )
    
    api_key = ""
    if api_provider != "Demo / Offline Mode":
        api_key = st.text_input(
            f"Enter {api_provider.split()[0]} API Key",
            type="password",
            help="Free API keys available from Groq Console or Hugging Face"
        )
    
    st.markdown("---")
    st.markdown("### 💡 Build for a Friend")
    st.info(
        "Built for friends struggling with exam cramming: Converts dense lecture notes into active-recall quizzes, flash summaries, and cheat sheets."
    )

# Header Section
st.markdown('<p class="main-header">🎓 StudyBuddy AI</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Transform dense lecture notes into interactive quizzes, flashcards & cheat-sheets using open-source AI.</p>', unsafe_allow_html=True)

# Main Input Section
col_input, col_settings = st.columns([3, 1])

with col_input:
    notes_text = st.text_area(
        "📝 Paste Lecture Notes, Topic, or Study Material:",
        height=220,
        placeholder="Example: Paste paragraphs from your Operating Systems, Distributed Systems, Database, or ML notes here..."
    )

with col_settings:
    st.markdown("### 🎯 Output Controls")
    quiz_count = st.slider("Number of Quiz Questions", min_value=3, max_value=10, value=5)
    difficulty = st.selectbox("Difficulty Level", ["Beginner / Conceptual", "Exam-Level Intermediate", "Advanced Technical"])
    generate_btn = st.button("🚀 Generate Study Kit", type="primary", use_container_width=True)

# Helper function to call Open-Weight LLMs
def call_open_model(prompt: str, provider: str, key: str) -> str:
    if provider == "Demo / Offline Mode" or not key:
        # Pre-computed high-quality mock response for demo
        return json.dumps({
            "summary": [
                "Core Concept: Distributed systems coordinate decentralized nodes via consensus protocols (e.g. Raft/Paxos) to ensure consistency.",
                "Concurrency Control: Race conditions occur when asynchronous tasks concurrently access shared mutable state without proper locking or atomic guarantees.",
                "Fault Tolerance: Heartbeat mechanisms and exponential backoff retry strategies ensure node recovery without cascading failures.",
                "Storage Decoupling: Modern microservices decouple compute instances from persistent state using distributed cache layers like Redis."
            ],
            "cheat_sheet": [
                {"term": "CAP Theorem", "definition": "A distributed data store can only provide at most two out of three guarantees: Consistency, Availability, and Partition tolerance."},
                {"term": "Eventual Consistency", "definition": "If no new updates are made, all replicas will eventually become consistent."},
                {"term": "Idempotency", "definition": "An operation that can be applied multiple times without changing the result beyond the initial application."}
            ],
            "quiz": [
                {
                    "question": "Which two guarantees does the CAP theorem state a distributed system can achieve simultaneously during network partition?",
                    "options": ["Consistency & Availability", "Consistency & Partition Tolerance (CP) or Availability & Partition Tolerance (AP)", "Speed & Fault Tolerance", "Atomic Isolation & Durability"],
                    "answer": 1,
                    "explanation": "When a network partition (P) occurs, the system must choose between Consistency (C) or Availability (A)."
                },
                {
                    "question": "What is the primary role of a heartbeat signal in distributed worker clusters?",
                    "options": ["To encrypt network traffic", "To track node liveness and detect dead worker instances", "To compile Python bytecode", "To balance database write queries"],
                    "answer": 1,
                    "explanation": "Heartbeat packets indicate node health; missing heartbeats trigger failover procedures."
                },
                {
                    "question": "Why is idempotency critical in message queues like Celery/RabbitMQ?",
                    "options": ["It reduces CPU temperature", "It allows safe retry of messages on failure without side-effects", "It turns synchronous calls into async", "It formats logs into JSON"],
                    "answer": 1,
                    "explanation": "At-least-once message delivery can cause duplicates; idempotent handlers prevent repeated mutations."
                }
            ]
        })
    
    if "Groq" in provider:
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
        payload = {
            "model": "llama-3.1-8b-instant",
            "messages": [
                {"role": "system", "content": "You are StudyBuddy AI. Return strictly valid JSON with keys: 'summary' (list of strings), 'cheat_sheet' (list of objects with 'term' and 'definition'), and 'quiz' (list of objects with 'question', 'options' list of 4 items, 'answer' 0-indexed integer, 'explanation' string)."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.3,
            "response_format": {"type": "json_object"}
        }
        res = requests.post(url, headers=headers, json=payload, timeout=25)
        if res.status_code == 200:
            return res.json()["choices"][0]["message"]["content"]
        else:
            raise Exception(f"API Error ({res.status_code}): {res.text}")

    return "{}"

# Generation Logic
if generate_btn:
    if not notes_text.strip():
        st.warning("⚠️ Please paste some notes or study material first!")
    else:
        with st.spinner("🤖 Open-weight AI model is generating your study kit..."):
            prompt = f"""
            Analyze the following study material and generate:
            1. 4-5 bullet key points summary.
            2. 3-5 core glossary cheat-sheet terms with concise definitions.
            3. Exactly {quiz_count} high-yield multiple-choice questions ({difficulty}) with 4 distinct options, the 0-indexed correct answer, and an explanation.

            Material:
            {notes_text}
            """
            try:
                raw_json = call_open_model(prompt, api_provider, api_key)
                data = json.loads(raw_json)
                st.session_state["study_data"] = data
                st.session_state["user_answers"] = {}
                st.success("✨ Study Kit Generated Successfully!")
            except Exception as e:
                st.error(f"Error generating study kit: {e}")

# Display Results
if "study_data" in st.session_state:
    data = st.session_state["study_data"]
    
    tab_summary, tab_quiz, tab_cheatsheet = st.tabs(["📋 Quick Summary", "🧠 Active-Recall Quiz", "📌 Flash Cheat-Sheet"])
    
    with tab_summary:
        st.subheader("Key Takeaways")
        for point in data.get("summary", []):
            st.markdown(f"- {point}")
            
    with tab_cheatsheet:
        st.subheader("Essential Glossary & Cheat-Sheet")
        for item in data.get("cheat_sheet", []):
            with st.container():
                st.markdown(f"**{item.get('term')}**: {item.get('definition')}")
                st.divider()

    with tab_quiz:
        st.subheader("Interactive Quiz")
        st.caption("Select your answers and click Submit to check your score!")
        
        quiz_items = data.get("quiz", [])
        user_answers = {}
        
        with st.form("quiz_form"):
            for i, q in enumerate(quiz_items):
                st.markdown(f"**Q{i+1}: {q.get('question')}**")
                options = q.get("options", [])
                user_choice = st.radio(
                    f"Select answer for Q{i+1}:",
                    options=range(len(options)),
                    format_func=lambda idx, opts=options: opts[idx] if idx < len(opts) else "",
                    key=f"q_{i}",
                    label_visibility="collapsed"
                )
                user_answers[i] = user_choice
                st.write("")
            
            submitted = st.form_submit_button("📊 Submit & Grade Quiz", type="primary")
            
        if submitted:
            score = 0
            st.markdown("### 🏆 Your Results")
            for i, q in enumerate(quiz_items):
                ans = user_answers.get(i)
                correct = q.get("answer")
                if ans == correct:
                    score += 1
                    st.success(f"**Q{i+1}: Correct!** ✅ — {q.get('explanation')}")
                else:
                    correct_opt = q.get("options", [])[correct] if correct < len(q.get("options", [])) else ""
                    st.error(f"**Q{i+1}: Incorrect!** ❌ (Correct Answer: *{correct_opt}*) — {q.get('explanation')}")
            
            st.metric(label="Final Score", value=f"{score} / {len(quiz_items)}", delta=f"{int(score/len(quiz_items)*100)}%")
            if score == len(quiz_items):
                st.balloons()
