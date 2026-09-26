import streamlit as st
import google.generativeai as genai

# Page Configuration
st.set_page_config(page_title="EduGenie - AI Learning Assistant", page_icon="🎓", layout="wide")

st.title("🎓 EduGenie: Gemini-Powered Learning Assistant")
st.write("Your personal AI tutor for summarizing concepts, generating quizzes, and solving doubts.")

# Sidebar for API Key Setup
st.sidebar.header("Configuration")
api_key = st.sidebar.text_input("Enter Google Gemini API Key:", type="password")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")

    # Mode Selector
    mode = st.sidebar.selectbox("Choose Learning Mode", ["Concept Explainer", "Quiz Generator", "Homework Helper"])

    # 1. Concept Explainer
    if mode == "Concept Explainer":
        st.subheader("💡 Topic Explainer & Study Notes")
        topic = st.text_input("Enter any topic or paste text to explain:")
        level = st.select_slider("Select Complexity Level:", options=["Beginner (Like I'm 10)", "Intermediate (College Level)", "Advanced (Expert)"])
        
        if st.button("Explain Topic"):
            if topic:
                prompt = f"Explain the topic '{topic}' for a {level} learner. Use key bullet points, concise explanations, and real-world examples."
                with st.spinner("EduGenie is thinking..."):
                    response = model.generate_content(prompt)
                    st.markdown(response.text)
            else:
                st.warning("Please enter a topic.")

    # 2. Quiz Generator
    elif mode == "Quiz Generator":
        st.subheader("📝 Practice Quiz Generator")
        subject = st.text_input("Enter subject or chapter topic:")
        num_q = st.slider("Number of Questions:", 1, 10, 5)
        
        if st.button("Generate Quiz"):
            if subject:
                prompt = f"Create a {num_q}-question multiple choice quiz on '{subject}'. Provide options (A, B, C, D) and reveal the correct answers at the end with brief explanations."
                with st.spinner("Generating quiz..."):
                    response = model.generate_content(prompt)
                    st.markdown(response.text)
            else:
                st.warning("Please enter a subject.")

    # 3. Homework Helper
    elif mode == "Homework Helper":
        st.subheader("❓ Doubts & Homework Assistance")
        question = st.text_area("Paste your problem, equation, or code snippet:")
        
        if st.button("Get Help"):
            if question:
                prompt = f"Act as an encouraging academic tutor. Solve or explain this problem step-by-step: {question}"
                with st.spinner("Analyzing problem..."):
                    response = model.generate_content(prompt)
                    st.markdown(response.text)
            else:
                st.warning("Please enter a question.")
else:
    st.info("👈 Please enter your Gemini API key in the sidebar to get started. Get a free API key from Google AI Studio (aistudio.google.com).")
