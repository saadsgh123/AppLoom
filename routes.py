import os
from datetime import timedelta
from flask import Flask, request, render_template, redirect, url_for, flash, jsonify, session
from models import storage
from models.job_app import JobApp
from authlib.integrations.flask_client import OAuth
import os
from dotenv import load_dotenv


load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
app.config['SESSION_COOKIE_NAME'] = 'google-login-session'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=5)

# oAuth Setup
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id=os.getenv("CLIENT_ID"),
    client_secret=os.getenv("CLIENT_SECRET"),
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',
    # This is only needed if using openId to fetch user info
    client_kwargs={'scope': 'email profile'},
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration'
)


@app.route('/')
def hello_world():
    email = dict(session)['profile']['email']
    return f'Hello, you are logged in as {email}!'


@app.route('/login')
def login():
    google = oauth.create_client('google')  # create the google oauth client
    redirect_uri = url_for('authorize', _external=True)
    return google.authorize_redirect(redirect_uri)


@app.route('/authorize')
def authorize():
    google = oauth.create_client('google')  # create the google oauth client
    token = google.authorize_access_token()  # Access token from google (needed to get user info)
    resp = google.get('userinfo')  # userinfo contains stuff u specificed in the scrope
    user_info = resp.json()
    user = oauth.google.userinfo()  # uses openid endpoint to fetch user info
    # Here you use the profile/user data that you got and query your database find/register the user
    # and set ur own data in the session not the profile from google
    session['profile'] = user_info
    session.permanent = True  # make the session permanant so it keeps existing after broweser gets closed
    return redirect('/')


@app.route('/logout')
def logout():
    for key in list(session.keys()):
        session.pop(key)
    return redirect('/')


@app.route('/jobs')
def jobs():
    users = storage.find_all(JobApp)
    return render_template('index.html', users=users)


@app.route('/check_result', methods=['GET'])
def check_result():
    return jsonify({"message": "Endpoint under construction"}), 501


@app.route('/add', defaults={'job_id': None})
@app.route('/add/<job_id>')
def add(job_id):
    jobapp = None
    if job_id:
        jobapp = storage.find_one(JobApp, {'id': job_id})
    return render_template('jobapp.html', jobapp=jobapp)


@app.route('/submit', methods=['POST'])
def submit():
    data = request.json
    if not data:
        return jsonify({"error": "Invalid input"}), 400

    required_fields = ['job_title', 'email', 'company', 'description']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    job_id = data.get('id')
    if job_id:
        job = storage.find_one(JobApp, {'id': job_id})
        if job:
            job['job_title'] = data.get('job_title')
            job['email'] = data.get('email')
            job['company'] = data.get('company')
            job['description'] = data.get('description')
            job_obj = JobApp(**job)
            job_obj.update()
    else:
        new_job = JobApp(
            job_title=data.get('job_title'),
            email=data.get('email'),
            company=data.get('company'),
            description=data.get('description')
        )
        new_job.save()

    return jsonify({"status": "success"})


@app.route('/delete/<job_id>', methods=['POST'])
def delete(job_id):
    job = storage.find_one(JobApp, {'id': job_id})
    if job:
        job_obj = JobApp(**job)
        job_obj.delete()
    return redirect(url_for('feed'))
