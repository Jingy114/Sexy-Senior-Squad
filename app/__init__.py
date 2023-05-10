from flask import Flask, render_template, request, redirect, url_for, session
from db import * 

app = Flask(__name__)
app.secret_key = "sss"

# @app.route("/", methods=['GET', 'POST'])
# def test():
#    return render_template('testing.html')

if __name__ == "__main__":
    app.debug = True
    app.run(port=1026)

@app.route("/", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = get_user(username)
        if user and user['password'] == password:
            session['username'] = username
            return redirect('/home')
        else:
            error_message = "Invalid credentials. Please try again."
            return render_template('login.html', error_message=error_message)
    else:
        return render_template('login.html')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if create_user(username, password):
            session['username'] = username
            return redirect('/home')
        else:
            error_message = "Registration failed. Please try again with a different username."
            return render_template('register.html', error_message=error_message)
    else:
        return render_template('register.html')


@app.route("/home")
def home():
    if 'username' in session:
        return render_template('home.html', username=session['username'])
    else:
        return redirect('/')


@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect('/')