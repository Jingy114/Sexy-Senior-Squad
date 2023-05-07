from flask import Flask, render_template, request, redirect, url_for, session
import json

app = Flask(__name__)
app.secret_key = "sss"

@app.route("/", methods=['GET', 'POST'])
def test():
    file = open("static/countries/country_data.json", "r")
    file_data = json.dumps(file.read())
    print(file_data)
    return render_template('testing.html', file_data = file_data)

if __name__ == "__main__":
    app.debug = True
    app.run()
