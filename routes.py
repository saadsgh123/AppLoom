from flask import Flask, request, render_template, redirect, url_for
from models import storage
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
        user = storage.find_one({'id': user_id})
        if user:
            user['username'] = request.form.get('username')
            user['email'] = request.form.get('email')
            storage.update_one({'id': user_id}, {'$set': user})
    else:
        username = request.form.get('username')
        email = request.form.get('email')
        new_user = User(username=username, email=email)
        new_user.save()

    return redirect("/")


@app.route("/delete/<user_id>", methods=['POST'])
def delete(user_id):
    if user_id:
        user = storage.find_one({'id': user_id})
        if user:
            storage.delete_one({'id': user_id})
    return render_template("/")



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
