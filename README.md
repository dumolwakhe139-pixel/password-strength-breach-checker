# Password Strength and Breach Checker
CodeForge BuildX 2026 mini project (Flask + HTML/CSS/JS).

## Run
    python -m venv venv
    venv\Scripts\activate        (Windows)   |   source venv/bin/activate  (Mac/Linux)
    pip install -r requirements.txt
    python app.py
Open http://127.0.0.1:5000

## Features
- Live strength score (0-6) with improvement tips
- Breach check using the Have I Been Pwned range API (k-anonymity)
- Tips page

## Structure
- app.py      Flask routes
- scorer.py   scoring rules
- breach.py   SHA-1 + k-anonymity breach lookup
- templates/  HTML pages
- static/     CSS and JavaScript
