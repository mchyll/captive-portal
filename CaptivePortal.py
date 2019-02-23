from flask import Flask, render_template


app = Flask(__name__)



@app.route('/login', methods=["GET", "POST"])
def login_page():
    return render_template("home.html")


@app.route('/')
def home():
    return render_template('login.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0')
