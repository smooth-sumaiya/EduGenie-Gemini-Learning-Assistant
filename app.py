import streamlit as st
import google.generativeai as genai

# Page Configuration
st.set_page_config(page_title="EduGenie - AI Learning Assistant", page_icon="🎓", layout="wide")

# Header Section
st.image("https://github.com/smooth-sumaiya/EduGenie-Gemini-Learning-Assistant/blob/main/image_4d9a0e77.jpg?raw=true", width=150)
st.title("🎓 EduGenie: Gemini-Powered Learning Assistant")
st.write("Your personal AI tutor for summarizing concepts, generating quizzes, and solving doubts.")

# Sidebar for API Key Setup
st.sidebar.header("Configuration")
api_key = st.sidebar.text_input("Enter Google Gemini API Key:", type="password")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-3.8-flash")

    # Create Tabs across the main view
    tab1, tab2, tab3 = st.tabs(["💡 Concept Explainer", "📝 Quiz Generator", "❓ Doubt Solver"])

    # TAB 1: Concept Explainer
    with tab1:
        st.subheader("Topic Explainer & Study Notes")
        topic = st.text_input("Enter any topic or paste text to explain:")
        complexity = st.select_slider("Select Complexity Level:", options=["Beginner (Like I'm 10)", "Intermediate", "Advanced (Expert)"])
        
        if st.button("Explain Topic"):
            if topic:
                prompt = f"Explain the following topic for a {complexity} level student: {topic}"
                response = model.generate_content(prompt)
                st.markdown(response.text)
            else:
                st.warning("Please enter a topic first.")

    # TAB 2: Quiz Generator
    with tab2:
        st.subheader("Interactive Quiz Generator")
        quiz_topic = st.text_input("Enter subject or topic for quiz:")
        num_questions = st.number_input("Number of questions:", min_value=1, max_value=10, value=5)
        
        if st.button("Generate Quiz"):
            if quiz_topic:
                prompt = f"Create a {num_questions}-question multiple-choice quiz on {quiz_topic} with an answer key at the bottom."
                response = model.generate_content(prompt)
                st.markdown(response.text)
            else:
                st.warning("Please enter a topic for the quiz.")

    # TAB 3: Doubt Solver
    with tab3:
        st.subheader("Instant Doubt Solver")
        doubt = st.text_area("Ask any specific question or problem:")
        
        if st.button("Solve Doubt"):
            if doubt:
                prompt = f"Provide a step-by-step clear explanation for this doubt: {doubt}"
                response = model.generate_content(prompt)
                st.markdown(response.text)
            else:
                st.warning("Please type your doubt first.")

else:
    st.info("👈 Please enter your Google Gemini API Key in the sidebar to get started.")
