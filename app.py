import streamlit as st
import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted, Unauthenticated, PermissionDenied, GoogleAPIError

# Page Configuration
st.set_page_config(page_title="EduGenie - AI Learning Assistant", page_icon="🎓", layout="wide")

# Header Section with Small Logo
st.image("https://github.com/smooth-sumaiya/EduGenie-Gemini-Learning-Assistant/blob/main/image_4d9a0e77.jpg?raw=true", width=150)
st.title("🎓 EduGenie: Gemini-Powered Learning Assistant")
st.write("Your personal AI tutor for summarizing concepts, generating quizzes, and solving doubts.")

# Sidebar for API Key Setup
st.sidebar.header("Configuration")
api_key = st.sidebar.text_input("Enter Google Gemini API Key:", type="password")

# Helper function to generate content with error handling
def safe_generate_content(model, prompt):
    try:
        response = model.generate_content(prompt)
        return response.text
    except ResourceExhausted:
        st.warning("⏳ Free tier rate limit reached (5 requests/minute). Please wait ~45 seconds and try again!")
    except (Unauthenticated, PermissionDenied):
        st.error("🔑 Invalid API Key. Please check your key in the sidebar and try again.")
    except GoogleAPIError as e:
        st.error(f"⚠️ Google API Error: {e}")
    except Exception as e:
        st.error(f"❌ An unexpected error occurred: {e}")
    return None

if api_key:
    try:
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
                if topic.strip():
                    with st.spinner("Generating explanation..."):
                        prompt = f"Explain the following topic for a {complexity} level student: {topic}"
                        result = safe_generate_content(model, prompt)
                        if result:
                            st.markdown(result)
                else:
                    st.warning("Please enter a topic first.")

        # TAB 2: Quiz Generator
        with tab2:
            st.subheader("Interactive Quiz Generator")
            quiz_topic = st.text_input("Enter subject or topic for quiz:")
            num_questions = st.number_input("Number of questions:", min_value=1, max_value=10, value=5)
            
            if st.button("Generate Quiz"):
                if quiz_topic.strip():
                    with st.spinner("Generating quiz..."):
                        prompt = f"Create a {num_questions}-question multiple-choice quiz on {quiz_topic} with an answer key at the bottom."
                        result = safe_generate_content(model, prompt)
                        if result:
                            st.markdown(result)
                else:
                    st.warning("Please enter a topic for the quiz.")

        # TAB 3: Doubt Solver
        with tab3:
            st.subheader("Instant Doubt Solver")
            doubt = st.text_area("Ask any specific question or problem:")
            
            if st.button("Solve Doubt"):
                if doubt.strip():
                    with st.spinner("Solving doubt..."):
                        prompt = f"Provide a step-by-step clear explanation for this doubt: {doubt}"
                        result = safe_generate_content(model, prompt)
                        if result:
                            st.markdown(result)
                else:
                    st.warning("Please type your doubt first.")

    except Exception as e:
        st.error(f"Failed to initialize model: {e}")

else:
    st.info("👈 Please enter your Google Gemini API Key in the sidebar to get started.")
