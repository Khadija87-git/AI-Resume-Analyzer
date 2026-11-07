from flask import Flask, render_template, request
from pypdf import PdfReader
import sqlite3
from datetime import datetime
from pathlib import Path

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024
DB_FILE = Path("resume_analyzer.db")

SKILLS = [
    "python", "java", "c++", "sql", "mysql", "html", "css", "javascript",
    "machine learning", "deep learning", "data analysis", "excel", "power bi",
    "communication", "teamwork", "problem solving", "git", "github",
    "flask", "django", "react", "linux", "data structures"
]

def initialize_database():
    with sqlite3.connect(DB_FILE) as con:
        con.execute("""
            CREATE TABLE IF NOT EXISTS analyses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                score INTEGER NOT NULL,
                matched_skills TEXT,
                missing_skills TEXT,
                created_at TEXT NOT NULL
            )
        """)

def read_resume(file):
    filename = file.filename.lower()
    if filename.endswith(".txt"):
        return file.read().decode("utf-8", errors="ignore")
    if filename.endswith(".pdf"):
        pdf = PdfReader(file)
        return "\n".join(page.extract_text() or "" for page in pdf.pages)
    raise ValueError("Please upload a PDF or TXT file.")

def detect_skills(text):
    text = text.lower()
    return sorted(skill for skill in SKILLS if skill in text)

def save_result(filename, score, matched, missing):
    with sqlite3.connect(DB_FILE) as con:
        con.execute(
            "INSERT INTO analyses(filename,score,matched_skills,missing_skills,created_at) VALUES(?,?,?,?,?)",
            (filename, score, ", ".join(matched), ", ".join(missing),
             datetime.now().strftime("%Y-%m-%d %H:%M"))
        )

@app.route("/", methods=["GET", "POST"])
def home():
    result, error = None, None
    if request.method == "POST":
        resume = request.files.get("resume")
        job_text = request.form.get("job_description", "")
        if not resume or not resume.filename:
            error = "Please select a resume file."
        elif not job_text.strip():
            error = "Please paste a job description."
        else:
            try:
                resume_text = read_resume(resume)
                if not resume_text.strip():
                    raise ValueError("No readable text found. Try a text-based PDF or TXT file.")
                resume_skills = detect_skills(resume_text)
                job_skills = detect_skills(job_text)
                matched = sorted(set(resume_skills) & set(job_skills))
                missing = sorted(set(job_skills) - set(resume_skills))
                score = round(len(matched) / len(job_skills) * 100) if job_skills else 0
                result = {"score": score, "resume": resume_skills,
                          "matched": matched, "missing": missing}
                save_result(resume.filename, score, matched, missing)
            except Exception as exc:
                error = str(exc)
    return render_template("index.html", result=result, error=error)

@app.route("/history")
def history():
    with sqlite3.connect(DB_FILE) as con:
        con.row_factory = sqlite3.Row
        rows = con.execute("SELECT * FROM analyses ORDER BY id DESC LIMIT 20").fetchall()
    return render_template("history.html", rows=rows)

initialize_database()

if __name__ == "__main__":
    app.run(debug=True)
