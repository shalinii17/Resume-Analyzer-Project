import fitz  # PyMuPDF
import re

# Common skills to match
common_skills = [
    "python", "java", "c++", "machine learning", "data analysis",
    "communication", "teamwork", "excel", "project management",
    "public speaking", "conflict management", "data analytics",
    "git", "sql", "html", "css", "docker", "tensorflow", "swift"
]

def extract_pdf_text(uploaded_file):
    """Extract all text from a PDF file using PyMuPDF"""
    with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
        text = ""
        for page in doc:
            text += page.get_text()
        return text

def extract_email(text):
    """Extract first email address from text"""
    pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    matches = re.findall(pattern, text)
    return matches[0] if matches else "Not found"

def extract_contact(text):
    """Extract first 10-digit phone number from text"""
    pattern = r"\b(?:\+91[-\s]?)?[0-9]{10}\b"
    matches = re.findall(pattern, text)
    return matches[0] if matches else "Not found"

def extract_name(text):
    """Try to extract name by checking the first few lines for capitalized words"""
    lines = text.strip().split('\n')
    for line in lines:
        line = line.strip()
        if len(line.split()) <= 5 and all(word[0].isupper() for word in line.split() if word.isalpha()):
            return line
    return "Not found"

def extract_skills(text):
    """Match known skills from resume text"""
    text = text.lower()
    found = []
    for skill in common_skills:
        if skill in text:
            found.append(skill)
    return list(set(found))      