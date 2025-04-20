from flask import Flask, render_template, request, redirect, url_for, session, send_file
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your_secret_key_here')  # Use environment variable for secret key
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///feedback.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Models
class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    enrollment_number = db.Column(db.String(20), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    teacher = db.Column(db.String(100), nullable=False)
    feedback_text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    date_submitted = db.Column(db.DateTime, default=datetime.utcnow)

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

# Create tables and default admin
with app.app_context():
    db.create_all()
    # Create default admin if not exists
    if not Admin.query.filter_by(username='admin').first():
        admin = Admin(username='admin', password='admin123')
        db.session.add(admin)
        db.session.commit()

# Constants
SUBJECTS = [
    ('MGT', 'MGT-Management'),
    ('PWP', 'PWP-Programming with Python'),
    ('MAD', 'MAD-Mobile Application Development'),
    ('ETI', 'ETI-Emerging Trends In Computer'),
    ('EDE', 'EDE-Entrepreneurship Development'),
    ('CPE', 'CPE-Capstone Project'),
    ('WBP', 'WBP-Web based Application Development using PHP')
]

TEACHERS = [
    'A.C. NAIK',
    'P.D.TANGDE',
    'V.B.BHOSALE',
    'S.B.LAHANE',
    'R.V.PATIL',
    'M.G.UNHALE',
    'P.P.ANGADI',
    'G.B.PAWAR',
    'ASHNA LOVEIN',
    'B.V.MACHAVE',
    'R.J.PATIL',
    'N.R.KULKARNI'
]

@app.route('/')
def index():
    return render_template('index.html', subjects=SUBJECTS, teachers=TEACHERS)

@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    if request.method == 'POST':
        name = request.form['name']
        enrollment_number = request.form['enrollment_number']
        subject = request.form['subject']
        teacher = request.form['teacher']
        feedback_text = request.form['feedback_text']
        rating = request.form['rating']

        new_feedback = Feedback(
            name=name,
            enrollment_number=enrollment_number,
            subject=subject,
            teacher=teacher,
            feedback_text=feedback_text,
            rating=int(rating)
        )
        db.session.add(new_feedback)
        db.session.commit()

        return redirect(url_for('thank_you'))

@app.route('/thank_you')
def thank_you():
    return render_template('thank_you.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        admin = Admin.query.filter_by(username=username, password=password).first()
        if admin:
            session['admin_logged_in'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            return render_template('admin_login.html', error='Invalid credentials')
    
    return render_template('admin_login.html')

@app.route('/admin/dashboard')
def admin_dashboard():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    feedbacks = Feedback.query.order_by(Feedback.date_submitted.desc()).all()
    return render_template('admin_dashboard.html', feedbacks=feedbacks)

@app.route('/admin/export_csv')
def export_csv():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    
    feedbacks = Feedback.query.all()
    data = []
    for feedback in feedbacks:
        data.append({
            'Date': feedback.date_submitted,
            'Name': feedback.name,
            'Enrollment Number': feedback.enrollment_number,
            'Subject': feedback.subject,
            'Teacher': feedback.teacher,
            'Feedback': feedback.feedback_text,
            'Rating': feedback.rating
        })
    
    df = pd.DataFrame(data)
    csv_file = 'feedbacks.csv'
    df.to_csv(csv_file, index=False)
    
    return send_file(
        csv_file,
        mimetype='text/csv',
        as_attachment=True,
        download_name='feedbacks.csv'
    )

@app.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('admin_login'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port) 