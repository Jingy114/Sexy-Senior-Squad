from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
app.secret_key = "sss"

@app.route("/", methods=['GET', 'POST'])
def test():
    return render_template('test.html')

if __name__ == "__main__":
    app.debug = True
    app.run()
