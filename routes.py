from flask import Flask, request, render_template, redirect, url_for, flash
from models import storage
from models.job_app import JobApp
from models.user import User

app = Flask(__name__)


@app.route('/')
def index():
    users = storage.find_all()
    return render_template('index.html', users=users)


@app.route('/add', defaults={'user_id': None})
@app.route('/add/<user_id>')
def add(user_id):
    user = None
    if user_id:
        # Fetch the user from storage if user_id is provided
        user = storage.find_one({'id': user_id})
    return render_template('add.html', user=user)  # Pass the full user object, not just user['id']


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
        username = request.form.get('username')
        email = request.form.get('email')
        new_job = JobApp(username=username, email=email)
        new_job.save()

    return redirect("/")


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
