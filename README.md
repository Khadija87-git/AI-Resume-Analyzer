# AI Resume Analyzer

A Python web application that compares skills found in a resume with skills mentioned in a job description. It displays matched and missing keywords, calculates a transparent match percentage, and saves analysis history locally.

## Features
- Upload a text-based PDF or TXT resume
- Paste a job description
- Detect skills from a built-in keyword list
- Display matched and missing skills
- Calculate a keyword match score
- Save the latest 20 analyses in SQLite

## Technologies
Python 3, Flask, SQLite, HTML, CSS, and pypdf.

## Run locally
1. Install Python 3.10 or newer.
2. Open a terminal in this project folder.
3. Create a virtual environment: `py -m venv .venv` (Windows) or `python3 -m venv .venv` (macOS/Linux).
4. Activate it: `.venv\Scripts\Activate.ps1` (Windows PowerShell) or `source .venv/bin/activate` (macOS/Linux).
5. Install packages: `pip install -r requirements.txt`
6. Run: `python app.py`
7. Open `http://127.0.0.1:5000` in your browser.

The SQLite database is created automatically.

## Scoring
Score = (matched job-description skills / detected job-description skills) × 100.
This is a keyword-based educational prototype, not a trained AI model, ATS simulator, or hiring decision tool. Scanned image-only PDFs may not contain extractable text.

## Privacy
Resume data is processed locally by this app. Do not upload real resumes, personal data, passwords, or generated database files to a public GitHub repository.
