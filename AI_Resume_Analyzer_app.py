# ===============================
# 🌈 AI Resume Analyzer (Final Pro UI Edition)
# Author: Zainab Ali ✨
# ===============================

import re
import io
import datetime
import pandas as pd
import streamlit as st
from PyPDF2 import PdfReader
from sqlalchemy import create_engine, Column, Integer, String, Float, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# 🎨 PAGE CONFIG
st.set_page_config(page_title="AI Resume Analyzer 💼", page_icon="🧠", layout="wide")

# 🌟 Custom CSS — elegant pastel theme
# 🌌 Premium Dark Theme CSS
st.markdown("""
<style>
/* ============================================
   💎 Elegant Polygon Gradient Theme
   Author: Zainab Ali | 2025 Edition
============================================ */

/* Smooth polygon-style gradient background */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #fbc2eb 0%, #a6c1ee 100%);
    background-attachment: fixed;
    background-repeat: no-repeat;
    color: #333;
    font-family: 'Poppins', sans-serif;
}

/* Page titles */
.main-title {
    text-align: center;
    font-size: 48px;
    font-weight: 800;
    color: #4a148c;
    margin-bottom: 10px;
    text-shadow: 0px 1px 3px rgba(0,0,0,0.15);
}
.subtitle {
    text-align: center;
    font-size: 40px;   /* make bigger — change to 24px if you want even larger */
    color: #000000;    /* black color */
    margin-bottom: 40px;
}
/* 💗 Elegant Pink Theme – Analyze Resume Button */
    div.stButton > button:first-child {
        background-color: #ff6b9f !important;   /* soft rose pink */
        color: purple !important;
        font-size: 18px !important;
        font-weight: 600 !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 12px 26px !important;
        box-shadow: 0 3px 10px rgba(255, 107, 159, 0.4);
        transition: all 0.3s ease-in-out;
    }

    /* 🌸 Hover – brighter pink glow */
    div.stButton > button:first-child:hover {
        background-color: #ff85b3 !important;  /* lighter pink */
        transform: translateY(-2px);
        box-shadow: 0 6px 18px rgba(255, 133, 179, 0.6);
    }
/* Card (Glass look) */
.card {
    background: rgba(255, 255, 255, 0.85);
    border-radius: 22px;
    padding: 25px 35px;
    box-shadow: 0 6px 20px rgba(0,0,0,0.15);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.4);
    margin-bottom: 25px;
}

/* Job card */
.job-card {
    background: rgba(255,255,255,0.9);
    border-left: 6px solid #ab47bc;
    border-radius: 14px;
    padding: 15px 18px;
    margin: 10px 0;
    box-shadow: 0 3px 10px rgba(0,0,0,0.1);
}
.job-title {
    color: #512da8;
    font-weight: 700;
    font-size: 18px;
}
.job-company {
    color: #e91e63;
    font-weight: 500;
}

/* Inputs */
.stTextInput > div > input,
.stTextArea > div > textarea {
    background-color: rgba(255,255,255,0.95) !important;
    border: 1px solid #ccc !important;
    border-radius: 10px !important;
    color: #333 !important;
    font-size: 16px !important;
    padding: 10px 14px !important;
}
label {
    color: #6a1b9a !important;
    font-weight: 600 !important;
}

/* Buttons - two styles: blue and pink hover */
.stButton>button {
    border: none;
    border-radius: 30px;
    padding: 12px 34px;
    font-size: 16px;
    font-weight: 600;
    cursor: pointer;
    transition: 0.4s;
    box-shadow: 0 4px 10px rgba(0,0,0,0.15);
}

/* Blue theme button */
.stButton>button:first-child {
    background: linear-gradient(90deg, #ffffff, #e3f2fd);
    color: #1976d2;
}
.stButton>button:first-child:hover {
    background: linear-gradient(90deg, #1976d2, #64b5f6);
    color: white;
}

/* Pink theme button */
.stButton>button:only-child,
.stButton>button:nth-child(2) {
    background: linear-gradient(90deg, #fce4ec, #f8bbd0);
    color: #e91e63;
}
.stButton>button:only-child:hover,
.stButton>button:nth-child(2):hover {
    background: linear-gradient(90deg, #e91e63, #f06292);
    color: white;
}

/* Footer */
.footer {
    text-align: center;
    color: #4a148c;
    font-size: 15px;
    margin-top: 40px;
}
/* 🔹 Make 'Upload PDF', 'Paste your resume text', 'Your Name', and 'Email Address' labels bigger */
[data-testid="stFileUploader"] label div,
[data-testid="stTextArea"] label div,
[data-testid="stTextInput"] label div {
    font-size:18px !important;
    font-weight: 600 !important;
   
}
/* ✨ Stylish animated hover for "Add Job" button */
button[kind="secondary"] {
    background: linear-gradient(90deg, #6a11cb, #2575fc);
    color: #fff !important;
    font-weight: 600;
    border: none !important;
    border-radius: 12px !important;
    padding: 10px 22px !important;
    box-shadow: 0 0 10px rgba(37,117,252,0.4);
    transition: all 0.4s ease-in-out;
}
/* ✨ Animated hover for "Add Job" form button */
div.stForm button {
    background: linear-gradient(90deg, #6a11cb, #2575fc);
    color: #fff !important;
    font-weight: 600 !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 10px 22px !important;
    box-shadow: 0 0 10px rgba(37,117,252,0.4);
    transition: all 0.4s ease-in-out;
}

div.stForm button:hover {
    background: linear-gradient(270deg, #2575fc, #6a11cb);
    transform: scale(1.07);
    box-shadow: 0 0 20px rgba(106,17,203,0.7);
}
[data-testid="stSidebar"] {
    background: rgba(255, 255, 255, 0.1);
    border-right: 1px solid rgba(255,255,255,0.15);
    color: #fff;
    font-family: 'Poppins', sans-serif;
}


</style>
""", unsafe_allow_html=True)


# 🧠 Header
st.markdown("<h1 class='main-title'>AI Resume Analyzer 💼</h1>", unsafe_allow_html=True)
st.markdown("<h4 class='subtitle'>Analyze your resume and find your dream job match using NLP & AI 🚀</h4>", unsafe_allow_html=True)

# ---------- DATABASE ----------
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    password_hash = Column(String)

class Job(Base):
    __tablename__ = 'jobs'
    job_id = Column(Integer, primary_key=True)
    title = Column(String)
    company = Column(String)
    skills_required = Column(Text)
    description = Column(Text)

class AnalysisResult(Base):
    __tablename__ = 'analysis_results'
    result_id = Column(Integer, primary_key=True)
    user_name = Column(String)
    user_email = Column(String)
    job_id = Column(Integer)
    match_score = Column(Float)
    missing_skills = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

ENGINE = create_engine('sqlite:///database.db', connect_args={"check_same_thread": False})
Base.metadata.create_all(ENGINE)
Session = sessionmaker(bind=ENGINE)
session = Session()

# 🌐 Insert sample jobs if none
def ensure_sample_jobs():
    if session.query(Job).count() == 0:
        jobs = [
            Job(title="Data Analyst", company="Google",
                skills_required="Python, SQL, Tableau, PowerBI, Excel",
                description="Analyze data and create reports."),
            Job(title="Machine Learning Engineer", company="Microsoft",
                skills_required="Python, Machine Learning, TensorFlow, PyTorch, Deep Learning",
                description="Build and deploy ML models."),
            Job(title="Backend Developer", company="Amazon",
                skills_required="Python, Django, REST API, MySQL, Docker",
                description="Develop scalable backend systems.")
        ]
        session.add_all(jobs)
        session.commit()
ensure_sample_jobs()

# ---------- NLP ----------
try:
    nlp = spacy.load("en_core_web_sm")
except:
    import subprocess, sys
    st.warning("Downloading spaCy model...")
    subprocess.run([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load("en_core_web_sm")

SKILL_KEYWORDS = [
    "python","sql","excel","tableau","powerbi","django","tensorflow",
    "pytorch","machine learning","deep learning","rest api","docker","mysql","pandas","numpy"
]
SKILL_PATTERN = re.compile(r'\\b(' + r'|'.join(SKILL_KEYWORDS) + r')\\b', re.I)

def extract_text_from_pdf(file):
    text = ""
    pdf = PdfReader(file)
    for page in pdf.pages:
        if page.extract_text():
            text += page.extract_text()
    return text

def extract_skills(text):
    found = SKILL_PATTERN.findall(text)
    return list(set([f.lower() for f in found]))

def match_resume_to_jobs(skills, jobs):
    resume_text = " ".join(skills)
    job_texts = [j.skills_required for j in jobs]
    vectorizer = TfidfVectorizer()
    tfidf = vectorizer.fit_transform([resume_text] + job_texts)
    sim = cosine_similarity(tfidf[0:1], tfidf[1:]).flatten()
    return sim

# ---------- UI ----------
col1, col2 = st.columns([1, 1.2])

with col1:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("📤 Upload or Paste Resume")
    pdf = st.file_uploader("Upload PDF", type=["pdf"])
    text_resume = st.text_area("Or paste your resume text", height=150)
    name = st.text_input("👤 Your Name")
    email = st.text_input("📧 Email Address")
    btn = st.button("🔍 Analyze Resume")
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("💼 Available Job Listings")
    jobs = session.query(Job).all()
    for j in jobs:
        st.markdown(f"""
        <div class='job-card'>
            <div class='job-title'>{j.title}</div>
            <div class='job-company'>@ {j.company}</div>
            <div><b>Skills:</b> {j.skills_required}</div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ---------- Resume Analysis ----------
if btn:
    text = ""
    if pdf: text += extract_text_from_pdf(pdf)
    if text_resume: text += text_resume
    if not text.strip():
        st.warning("⚠️ Please upload or paste your resume content first.")
    else:
        skills = extract_skills(text)
        similarities = match_resume_to_jobs(skills, jobs)
        idx = int(pd.Series(similarities).idxmax())
        best_job = jobs[idx]
        score = round(float(similarities[idx]) * 100, 2)
        job_skills = [s.strip().lower() for s in best_job.skills_required.split(",")]
        missing = [s for s in job_skills if s not in skills]
        missing_str = ", ".join(missing) if missing else "None"

        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.success(f"🎯 **Best Match:** {best_job.title} @ {best_job.company}")
        st.write(f"✅ **Match Score:** {score}%")
        st.write(f"🔍 **Missing Skills:** {missing_str}")
        st.markdown("</div>", unsafe_allow_html=True)

        record = AnalysisResult(user_name=name, user_email=email, job_id=best_job.job_id,
                                match_score=score, missing_skills=missing_str)
        session.add(record)
        session.commit()
        st.info("💾 Result saved successfully!")

# ---------- Add New Job Section ----------
st.markdown("---")
st.markdown("<h2 style='text-align:center; color:#4a148c;'>➕ Add a New Job Listing</h2>", unsafe_allow_html=True)

with st.form("add_job_form"):
    new_title = st.text_input("Job Title")
    new_company = st.text_input("Company Name")
    new_skills = st.text_area("Required Skills (comma separated)")
    new_desc = st.text_area("Job Description")
    submit_btn = st.form_submit_button("💾 Add Job")

    if submit_btn:
        if new_title and new_company and new_skills and new_desc:
            new_job = Job(title=new_title, company=new_company, skills_required=new_skills, description=new_desc)
            session.add(new_job)
            session.commit()
            st.success(f"✅ Job '{new_title}' added successfully!")
        else:
            st.error("⚠️ Please fill in all fields before submitting.")

# ---------- Sidebar (Enhanced Table View) ----------
st.sidebar.markdown("<h2 style='color:#f06292;'>📜 Recent Analyses</h2>", unsafe_allow_html=True)

recents = session.query(AnalysisResult).order_by(AnalysisResult.created_at.desc()).limit(5).all()

if recents:
    df_recent = pd.DataFrame([{
        "👤 Name": r.user_name,
        "📧 Email": r.user_email,
        "💼 Job ID": r.job_id,
        "🎯 Match (%)": f"{r.match_score:.2f}",
        "🕓 Date": r.created_at.strftime("%Y-%m-%d")
    } for r in recents])

    st.sidebar.dataframe(
        df_recent,
        use_container_width=True,
        hide_index=True
    )
else:
    st.sidebar.info("No recent analyses yet.")


# ---------- Footer ----------
st.markdown("<p class='footer'>Made with ❤️ by Zainab | AI Resume Analyzer 2025</p>", unsafe_allow_html=True)
