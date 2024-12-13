from flask import Flask, request, render_template

from models import storage
from models.user import User

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    # Retrieve form data
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    user = User(username=username, email=email, password=password)
    user.save()



    # Log the data for testing purposes
    app.logger.info(f"Received data: Username={username}, Email={email}, Password={password}")

    return f"Form submitted successfully! Received Username: {username}, Email: {email}."  # Simple confirmation message


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
