import time

from flask import Flask, request, render_template, redirect, url_for, flash, jsonify
from models import storage
from models.job_app import JobApp
from models.user import User

app = Flask(__name__)


@app.route('/')
def index():
    users = storage.find_all(JobApp)
    return render_template('index.html', users=users)




@app.route('/check_result', methods=['GET'])
def check_result():
    return None


@app.route('/add', defaults={'job_id': None})
@app.route('/add/<job_id>')
def add(job_id):
    jobapp = None
    if job_id:
        # Fetch the user from storage if job_id is provided
        jobapp = storage.find_one(JobApp, {'id': job_id})
    return render_template('jobapp.html', jobapp=jobapp)  # Pass the full user object, not just user['id']


@app.route('/submit', methods=['POST'])
@app.route('/submit/<job_id>', methods=['POST'])  # Accept job_id
def submit(job_id=None):
    data = request.json  # Parse JSON from the request body
    if job_id:
        # Update existing job
        job = storage.find_one({'id': job_id})
        if job:
            job['job_title'] = data.get('job-title')  # Use JSON keys
            job['email'] = data.get('email')
            job['company'] = data.get('company')
            job['description'] = data.get('description')
            job_obj = JobApp(**job)
            job_obj.update()
    else:
        # Add new job
        job_title = data.get('job-title')  # Use JSON keys
        email = data.get('email')
        company = data.get('company')
        description = data.get('description')
        new_job = JobApp(job_title=job_title, email=email, company=company, description=description)
        new_job.save()

    return jsonify({"status": "success"})



@app.route("/delete/<job_id>", methods=['POST'])
def delete(job_id):
    if job_id:
        job = storage.find_one({'id': job_id})
        if job:
            job_obj = JobApp(**job)
            job_obj.delete()
            # flash("User deleted successfully.", "success")
    return redirect(url_for('index'))


@app.route('/submit', methods=['POST'])
def submit():
    print("Request received at /submit")
    print("Request Data:", request.json)
    return jsonify({"status": "success"})





if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
