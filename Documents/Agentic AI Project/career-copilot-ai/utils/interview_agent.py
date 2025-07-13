import streamlit as st
from transformers import pipeline

@st.cache_resource
def load_interview_model():
    return pipeline("text-generation", model="microsoft/DialoGPT-medium")

interview_model = load_interview_model()

<<<<<<< HEAD
def run_mock_interview(user_input):
    if not user_input:
        return "Please enter a question."

    response = interview_model(user_input, max_length=100, num_return_sequences=1)
    return response[0]['generated_text']
=======
# Load classifier globally (better for Render)
classifier = pipeline(
    "text-classification",
    model="distilbert-base-uncased-finetuned-sst-2-english"
)

def generate_mock_interview_question(resume_data):
    """
    Select a random question based on resume data.
    """
    skills = resume_data.get("skills", [])
    if skills:
        selected = random.choice(TECHNICAL_QUESTIONS + BASIC_QUESTIONS)
    else:
        selected = random.choice(BASIC_QUESTIONS)
    return f"🎤 Interview Question: {selected}"

def analyze_interview_response(response):
    """
    Evaluate the quality of a user's interview answer.
    """
    try:
        result = classifier(response)
        label = result[0]["label"]
        score = result[0]["score"]
        sentiment = "✅ Positive" if label == "POSITIVE" else "⚠️ Needs Improvement"
        return f"🧠 Analysis: {sentiment} (Confidence: {score:.2f})"
    except Exception as e:
        return f"❌ Error analyzing response: {e}"
>>>>>>> b5338d4123ab822d91881e42e09544d4c406a755
