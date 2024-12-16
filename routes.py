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


@app.route('/add', defaults={'user_id': None})
@app.route('/add/<user_id>')
def add(user_id):
    user = None
    if user_id:
        # Fetch the user from storage if user_id is provided
        user = storage.find_one(JobApp, {'id': user_id})
    return render_template('jobapp.html', user=user)  # Pass the full user object, not just user['id']


@app.route('/submit', methods=['POST'])
@app.route('/submit/<user_id>', methods=['POST'])  # Accept user_id
def submit(user_id=None):
    if user_id:
        # Update existing user
        job = storage.find_one({'id': user_id})
        if job:
            job['username'] = request.form.get('username')
            job['email'] = request.form.get('email')
            job_obj = JobApp(**job)
            job_obj.update()
    else:
        job_title = request.form.get('job-title')
        email = request.form.get('email')
        company = request.form.get('company')
        description = request.form.get('description')
        new_job = JobApp(job_title=job_title, email=email, company=company, description=description)
        new_job.save()

    return jsonify({"status": "success"})


@app.route("/delete/<user_id>", methods=['POST'])
def delete(user_id):
    if user_id:
        job = storage.find_one({'id': user_id})
        if job:
            job_obj = JobApp(**job)
            job_obj.delete()
            # flash("User deleted successfully.", "success")
    return redirect(url_for('index'))




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
