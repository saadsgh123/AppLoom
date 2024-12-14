from flask import Flask, request, render_template, redirect

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
        user = storage.find_one({'id': user_id})
    return render_template('add.html', user=user)



@app.route('/submit', methods=['POST'])
def submit():
    # Retrieve form data
    username = request.form.get('username')
    email = request.form.get('email')
    user = storage.find_one({"username": 'saadsgh', "email": 'mehdi.nasser@gmail.com'})
    print("User", user)
    user_obj = User(user)
    print("USER_OBJ", user_obj)
    if user:
        user_obj.update()
    else:
        user_obj.save()

    return redirect("/")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
