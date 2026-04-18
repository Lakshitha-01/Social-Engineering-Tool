# Social Engineering Simulation Tool (Flask Web App)

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
- **Utilities:** threading, subprocess, requests, webbrowser

---

## Project Structure
