from resume_parser import extract_pdf_text, extract_email, extract_contact, extract_name, extract_skills

import streamlit as st
import fitz  # PyMuPDF
import re
import pandas as pd
from datetime import datetime

# ========== PAGE CONFIG ==========
st.set_page_config(page_title="Resume Analyzer", layout="centered")

# ========== SIDEBAR ==============
st.sidebar.title("Login")
user_type = st.sidebar.radio("Choose Mode:", ("User", "Admin"))

# ========== ADMIN MODE ============
if user_type == "Admin":
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")

    if st.sidebar.button("Login"):
        if username == "admin" and password == "1234":
            st.markdown("<h2 style='color: #8A2BE2;'>📊 Admin Dashboard</h2>", unsafe_allow_html=True)
            st.info("You are viewing stored user analysis records.")

            try:
                df = pd.read_csv("user_data.csv")
                st.dataframe(df)
                st.success(f"Total Users: {len(df)}")
            except FileNotFoundError:
                st.warning("No user data found yet.")
        else:
            st.error("Invalid credentials")

# ========== USER MODE ============
if user_type == "User":
    st.markdown("<h1 style='text-align: center; color: #4CAF50;'>📄 Resume Analyzer</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Upload your resume & paste job description for personalized feedback</p>", unsafe_allow_html=True)
    st.markdown("---")

    # --- Skill list ---
    common_skills = [
        "python", "java", "c++", "machine learning", "data analysis",
        "communication", "teamwork", "excel", "project management",
        "public speaking", "conflict management", "data analytics",
        "git", "sql", "html", "css", "docker", "tensorflow", "swift"
    ]

    # --- Courses for Skills ---
    course_links = {
        "docker": "https://www.coursera.org/learn/docker",
        "react": "https://www.udemy.com/course/react-the-complete-guide/",
        "aws": "https://www.aws.training/",
        "sql": "https://www.codecademy.com/learn/learn-sql",
        "typescript": "https://www.udemy.com/course/typescript/",
        "git": "https://www.coursera.org/learn/introduction-git-github",
        "python": "https://www.udemy.com/course/complete-python-bootcamp/",
        "machine learning": "https://www.coursera.org/learn/machine-learning",
    }

    # --- Helpers ---
    def extract_pdf_text(uploaded_file):
        with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
            return "".join([page.get_text() for page in doc])

    def extract_email(text):
        match = re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}", text)
        return match[0] if match else "Not found"

    def extract_contact(text):
        match = re.findall(r"\\b(?:\\+91[-\\s]?)?[0-9]{10}\\b", text)
        return match[0] if match else "Not found"

    def extract_name(text):
        lines = text.strip().split('\n')
        for line in lines:
            line = line.strip()
            if len(line.split()) <= 5 and all(w[0].isupper() for w in line.split() if w.isalpha()):
                return line
        return "Not found"

    def extract_skills(text):
        text = text.lower()
        return list(set(skill for skill in common_skills if skill in text))

    # --- Interface ---
    uploaded_file = st.file_uploader("📤 Upload your resume (PDF)", type=["pdf"])
    job_description = st.text_area("📝 Paste the job description here")

    if st.button("🔍 Analyze"):
        if uploaded_file and job_description:
            with st.spinner("Analyzing..."):
                resume_text = extract_pdf_text(uploaded_file)
                name = extract_name(resume_text)
                email = extract_email(resume_text)
                contact = extract_contact(resume_text)

                resume_skills = extract_skills(resume_text)
                job_skills = extract_skills(job_description)

                matched_skills = set(resume_skills) & set(job_skills)
                missing_skills = set(job_skills) - set(resume_skills)

                match_percentage = round((len(matched_skills) / len(job_skills)) * 100, 2) if job_skills else 0.0

                recommended_courses = {
                    skill: course_links[skill]
                    for skill in missing_skills if skill in course_links
                }

            # --- Display ---
            st.success("✅ Analysis Complete!")

            st.markdown("### 👤 Basic Information")
            st.write(f"**Name:** {name}")
            st.write(f"**Email:** {email}")
            st.write(f"**Contact:** {contact}")

            st.markdown("---")

            st.markdown("### 🧠 Skills Recommendation")

            # --- Current Skills ---
            st.markdown("**✅ Current Skills from Resume:**")
            if resume_skills:
                st.markdown(
                    " ".join([f"<span style='background-color:#d4edda;color:#155724;padding:8px 12px;margin:4px;border-radius:20px;display:inline-block;font-size:16px'>{skill}</span>"
                            for skill in resume_skills]),
                    unsafe_allow_html=True
                )
            else:
                st.write("No skills found in resume.")

            # --- Missing Skills ---
            st.markdown("**❌ Missing Skills (Required in Job Description):**")
            if missing_skills:
                st.markdown(
                    " ".join([f"<span style='background-color:#f8d7da;color:#721c24;padding:8px 12px;margin:4px;border-radius:20px;display:inline-block;font-size:16px'>{skill}</span>"
                            for skill in missing_skills]),
                    unsafe_allow_html=True
                )
            else:
                st.success("You're matching all the required skills! 🎉")

            st.markdown("### 📊 Match Percentage")
            st.progress(match_percentage / 100)
            st.success(f"Match Score: {match_percentage}%")

            with st.expander("🎓 Course Recommendations"):
                if recommended_courses:
                    for skill, link in recommended_courses.items():
                        st.markdown(f"- **{skill.capitalize()}**: [{link}]({link})")
                else:
                    st.write("You're all set! 🎉")

            with st.expander("🎥 Resume Writing Tips"):
                st.markdown("- 📌 [Resume Tips for Freshers](https://www.youtube.com/watch?v=IIGWpw1FXhk)")
                st.markdown("- 📌 [Top Resume Mistakes to Avoid](https://www.youtube.com/watch?v=NUhDP30IRKk)")
                st.markdown("- 📌 [How to Write a Resume That Gets Noticed](https://www.youtube.com/watch?v=QnUI3sLZ4hc)")

            # --- Save User Info ---
            user_row = {
                "Name": name,
                "Email": email,
                "Match %": match_percentage,
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            try:
                df_existing = pd.read_csv("user_data.csv")
                df_existing = pd.concat([df_existing, pd.DataFrame([user_row])], ignore_index=True)
            except FileNotFoundError:
                df_existing = pd.DataFrame([user_row])

            df_existing.to_csv("user_data.csv", index=False)

        else:
            st.warning("⚠️ Please upload a resume and enter a job description.")

# Optional: Hide Streamlit branding
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)


