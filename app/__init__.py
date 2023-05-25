from flask import Flask, render_template, request, redirect, url_for, session
from db import *
from databases import *

app = Flask(__name__)
app.secret_key = "sss"

# @app.route("/", methods=['GET', 'POST'])
# def test():
#    return render_template('testing.html')


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

# Testing route


@app.route("/testing", methods=['GET', 'POST'])
def testing():
    return render_template('home.html')

# Loading Data Set


@app.route("/load/<dataset>", methods=['POST'])
def load_dataset(dataset):
    # json_dataset = {'dataset'dataset}
    print(request.form[""])
    return redirect("/testing")  # , dataset=json_dataset)


@app.route('/form-submit/<dataset>', methods=['GET', 'POST'])
def handleFormSubmission(dataset):
    data_selected = dataset
    db_manager = DatabaseManager('my_database.db')
    data_by_country = db_manager.select_all_data(data_selected, '*')
    all_data = db_manager.select_all_data(data_selected, data_selected)
    # data_by_country = db_manager.select_all_data('my_table', 'country, ' + data_selected)
    # all_data = db_manager.select_all_data('my_table', data_selected)
    # data_by_country = db_manager.select_all_data(data_selected, '*')
    print(data_by_country)
    db_manager.close()
    max = 0
    for data in all_data:
        value = data[0]
        if isinstance(value, str):
            value = float(value)
        elif not isinstance(value, float):
            return [False]
        if value > max:
            max = value
    sanitized_data = []
    # print(data_by_country)
    for data in data_by_country:
        original_country_name = data[0]
        country_name = original_country_name.replace(" ", "").lower()
        sanitized_data.append((country_name, data[1]))
    # print(sanitized_data)
    return [True, dict(sanitized_data), max, data_selected]


@app.route('/large-form-submit', methods=['GET', 'POST'])
def handleLargeFormSubmission():
    dataset = request.form.get('dataset1')
    dataset2 = request.form.get('dataset2')
    operand = request.form.get('operand')
    # operation = ???
    db_manager = DatabaseManager('my_database.db')
    data_by_country = db_manager.select_all_data(dataset, '*')
    data_by_country2 = db_manager.select_all_data(
        dataset2, '*')
    db_manager.close()
    # print(data_by_country)
    sanitized_data = []
    for data in data_by_country:
        original_country_name = data[0]
        country_name = original_country_name.replace(" ", "").lower()
        value = data[1]
        if isinstance(value, str):
            value = float(value)
        elif not isinstance(value, float):
            return [False]
        sanitized_data.append((country_name, value))
    dict_of_data = dict(sanitized_data)
    max = 0
    complete_sanitized_data = []
    for data in data_by_country2:
        original_country_name = data[0]
        country_name = original_country_name.replace(" ", "").lower()
        if country_name not in dict_of_data.keys():
            pass
        value = dict_of_data[country_name]
        value2 = data[1]
        if isinstance(value2, str):
            value2 = float(value)
        elif not isinstance(value2, float):
            return [False]
        if operand == 'Added To':
            new_value = value + value2
        elif operand == 'Subtracted From':
            new_value = value - value2
        elif operand == 'Divided By':
            new_value = value / value2
        else:
            new_value = value * value2
        if new_value > max:
            max = new_value
        complete_sanitized_data.append((country_name, new_value))
    return [True, dict(complete_sanitized_data), max]


if __name__ == "__main__":
    app.debug = True
    app.run(port=1026)
