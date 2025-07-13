import streamlit as st
from transformers import pipeline

<<<<<<< HEAD
@st.cache_resource
def load_generator():
    return pipeline("text-generation", model="gpt2")

generator = load_generator()
=======
# Use a more suitable model for text generation
generator = pipeline(
    "text-generation",
    model="gpt2",  # You can also try 'EleutherAI/gpt-neo-125M' or 'tiiuae/falcon-7b-instruct' if memory allows
    tokenizer="gpt2"
)

def generate_cover_letter(resume_text, job_description):
    """
    Generate a concise, professional cover letter from resume and JD.
    """
    resume_text = resume_text[:1000]
    job_description = job_description[:1000]

    prompt = f"""
Write a concise and professional cover letter tailored to the following job.
>>>>>>> b5338d4123ab822d91881e42e09544d4c406a755

def generate_cover_letter(resume_text, job_description):
    if not resume_text or not job_description:
        return "Please provide both resume and job description to generate a cover letter."

<<<<<<< HEAD
    prompt = (
        "Write a professional and personalized cover letter based on the following resume and job description:\n\n"
        f"Resume:\n{resume_text}\n\n"
        f"Job Description:\n{job_description}\n\n"
        "Cover Letter:"
    )

    output = generator(prompt, max_length=300, do_sample=True, temperature=0.7, num_return_sequences=1)
    return output[0]['generated_text']
=======
Candidate Resume:
{resume_text}

Cover Letter:
"""

    try:
        output = generator(prompt, max_length=400, num_return_sequences=1, do_sample=True)
        letter = output[0]["generated_text"].replace(prompt, "").strip()
        return letter
    except Exception as e:
        return f"❌ Error generating cover letter: {e}"
>>>>>>> b5338d4123ab822d91881e42e09544d4c406a755
