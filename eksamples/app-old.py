from flask import Flask, render_template, request, session, flash
import pymysql

import os
import gc


def db_connect():

    try:
        import credentials
        password = credentials.login['password']
    except ImportError:
        if "MEDLEMSREGISTER_PASSWORD" in os.environ:
            password = os.environ["MEDLEMSREGISTER_PASSWORD"]
        else:
            with open("/home/staff/drift/passord/db-medlemsregister") as f:
                password = f.readline().rstrip('\n')

    conn = pymysql.connect(host="tihlde.org",
                           user="medlemsregister",
                           password=password,
                           database="medlemsregister",
                           charset='utf8')
    c = conn.cursor()
    return c, conn


# Create valid_login
def valid_login(username):
    if not username:
        return 0

    try:
        c, conn = db_connect()
        c.execute('SELECT aktivert FROM members WHERE histbruker = %s', (username,))
        result = c.fetchone()
        return result

    finally:
        c.close()
        conn.close()
        gc.collect()


def get_name(username):
    if not username:
        return 0

    try:
        c, conn = db_connect()
        c.execute('SELECT fornavn, etternavn FROM members WHERE histbruker = %s', (username,))
        result = c.fetchone()
        return result

    finally:
        c.close()
        conn.close()
        gc.collect()


app = Flask(__name__)


@app.route('/')
def home():
    if session.get('loged_in'):
        return render_template('home.html')

    return render_template('login.html')


@app.route('/login', methods=["GET", "POST"])
def login_page():
    if session.get('username'):
        username = session.get('username')
        first_name, last_name = get_name(username)
        return render_template("home.html", name=first_name + ' ' + last_name, username=username)

    if 'username' not in request.form:
        return render_template('login.html')

    username = request.form['username']
    if valid_login(username):
        session['logged_in'] = True
        session['username'] = username
        first_name, last_name = get_name(username)
        return render_template("home.html", name=first_name+' '+last_name, username=username)
    else:
        flash("User not found or deactivated\nTry again.")
        return render_template('login.html')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    flash("You have been logged out!")
    gc.collect()
    return render_template('login.html')


if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(host='0.0.0.0')
