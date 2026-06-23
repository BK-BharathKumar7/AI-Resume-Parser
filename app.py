import streamlit as st
import pdfplumber
import pandas as pd
import re

st.set_page_config(page_title="AI Resume Parser", page_icon="📄")

st.title("📄 AI Resume Parser System")

# Skills Database
SKILLS = [
    "Python", "Java", "C++", "C", "SQL",
    "HTML", "CSS", "JavaScript",
    "React", "Node.js", "Angular",
    "Machine Learning", "Deep Learning",
    "Data Science", "TensorFlow", "PyTorch",
    "Git", "Linux", "AWS",
    "Docker", "Kubernetes",
    "Data Structures", "Algorithms"
]

uploaded_file = st.file_uploader(
    "Upload Resume (PDF)",
    type=["pdf"]
)

def extract_text(pdf_file):
    text = ""

    try:
        with pdfplumber.open(pdf_file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()

                if page_text:
                    text += page_text + "\n"

    except Exception as e:
        st.error(f"Error reading PDF: {e}")

    return text

def extract_email(text):
    email_pattern = r'[\w\.-]+@[\w\.-]+\.\w+'

    match = re.search(email_pattern, text)

    return match.group() if match else "Not Found"

def extract_phone(text):
    phone_pattern = r'(\+?\d[\d\s\-\(\)]{8,15}\d)'

    match = re.search(phone_pattern, text)

    return match.group().strip() if match else "Not Found"

def extract_name(text):
    lines = text.split("\n")

    for line in lines[:10]:

        line = line.strip()

        if (
            len(line.split()) >= 2
            and len(line.split()) <= 4
            and "@" not in line
            and not any(char.isdigit() for char in line)
        ):
            return line

    return "Not Found"

def extract_skills(text):

    found_skills = []

    text_lower = text.lower()

    for skill in SKILLS:

        if skill.lower() in text_lower:
            found_skills.append(skill)

    return list(set(found_skills))

def extract_education(text):

    education_keywords = [
        "B.E",
        "B.Tech",
        "M.Tech",
        "B.Sc",
        "M.Sc",
        "Bachelor",
        "Master",
        "Diploma",
        "HSC",
        "SSLC",
        "CBSE"
    ]

    found = []

    text_lower = text.lower()

    for item in education_keywords:

        if item.lower() in text_lower:
            found.append(item)

    return found

if uploaded_file:

    text = extract_text(uploaded_file)

    if text:

        name = extract_name(text)
        email = extract_email(text)
        phone = extract_phone(text)
        skills = extract_skills(text)
        education = extract_education(text)

        st.subheader("Extracted Information")

        st.write(f"**Name:** {name}")
        st.write(f"**Email:** {email}")
        st.write(f"**Phone:** {phone}")

        st.write("### Skills")

        if skills:
            for skill in skills:
                st.write("✅", skill)
        else:
            st.write("No skills detected")

        st.write("### Education")

        if education:
            for edu in education:
                st.write("🎓", edu)
        else:
            st.write("No education details detected")

        result = pd.DataFrame({
            "Field": [
                "Name",
                "Email",
                "Phone",
                "Skills",
                "Education"
            ],
            "Value": [
                name,
                email,
                phone,
                ", ".join(skills),
                ", ".join(education)
            ]
        })

        csv = result.to_csv(index=False)

        st.download_button(
            "⬇ Download Results",
            csv,
            "resume_data.csv",
            "text/csv"
        )
