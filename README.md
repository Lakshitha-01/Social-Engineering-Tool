# Social Engineering Simulation Tool

## Overview
This project is a Flask-based web application designed to simulate a multi-step email and landing-page workflow. It demonstrates backend development, form handling, dynamic routing, and email automation using Python. The system guides a user through selecting an email template, customizing content, choosing a landing page, and sending an email.

⚠️ **Note:** This project is intended strictly for educational and cybersecurity awareness demonstration purposes in a controlled environment.

---

## Features

- Multi-step user workflow (Step 1 → Step 2 → Preview → Send)
- Dynamic email template customization
- Landing page selection based on user input
- Automated email sending using SMTP
- Dynamic routing for landing pages
- Form data handling and processing
- Basic data logging to local file
- Ngrok integration for public URL exposure during testing
- Browser auto-launch on server start

---

## Tech Stack

- **Backend:** Python, Flask
- **Email Service:** smtplib, email.message
- **Frontend:** HTML, CSS, JavaScript (Jinja templates)
- **Tunneling:** Ngrok
- **Build Tool:** PyInstaller  
- **Utilities:** threading, subprocess, requests, webbrowser

---

## Setup Instructions

### 1. Clone the repository
```
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```
### 2. Intsall dependencies
```
pip install -r requirements.txt
```
### 3. Run the application
```
python app.py
```

## Executable Version
The project includes a packaged executable version:
```
dist/app.exe
```
This allows running the application without manually starting Python.

---

## How It Works

1. **Step 1:** User selects email template and enters basic content
2. **Step 2:** User selects target landing page or brand context
3. **Preview:** System generates final email preview
4. **Send:** Email is sent using SMTP with dynamically generated content
5. **Landing Page:** Displays selected HTML page and captures submitted form data
