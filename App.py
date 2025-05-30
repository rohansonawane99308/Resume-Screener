import streamlit as st
import os
import uuid
from resume_parser.parser import extract_text_from_pdf, extract_skills
from jd_matcher.matcher import get_similarity_score
import pandas as pd

st.set_page_config(layout="wide")
st.title("🔍 Resume Matcher and Skill Extractor")

jd_input = st.text_area("Paste Job Description", height=200)

uploaded_files = st.file_uploader("Upload Resume PDFs", type=["pdf"], accept_multiple_files=True)

if st.button("Match Resumes"):
    if not jd_input or not uploaded_files:
        st.warning("Please upload resumes and enter JD text.")
    else:
        results = []
        for resume_file in uploaded_files:
            file_bytes = resume_file.read()
            temp_filename = f"temp_{uuid.uuid4().hex}.pdf"
            with open(temp_filename, "wb") as f:
                f.write(file_bytes)

            resume_text = extract_text_from_pdf(temp_filename)
            score = get_similarity_score(resume_text, jd_input)
            skills = extract_skills(resume_text)

            results.append({
                "Filename": resume_file.name,
                "Score": round(score, 3),
                "Skills": ", ".join(skills)
            })

            os.remove(temp_filename)

        df = pd.DataFrame(results).sort_values(by="Score", ascending=False)

        def color_score(val):
            if val >= 0.75:
                return 'background-color: #a8e6cf'
            elif val >= 0.5:
                return 'background-color: #ffd3b6'
            else:
                return 'background-color: #ffaaa5'

        st.dataframe(df.style.applymap(color_score, subset=['Score']))
