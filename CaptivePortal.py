from flask import Flask, render_template, request, flash, redirect
import sqlite3
import os
import ipa_auth as ipa
import db
import ip_management

app = Flask(__name__)


def ban_user(user):
    # Disallow internet access for all IPs associated with the user
    for ip in db.getIPsForUser(user):
        ip_management.iptables_disallow_ip(ip)

    if db.banUser(user):
        return True

    return False


@app.route('/admin', methods=["GET"])
def admin_page():

    ip = request.environ['REMOTE_ADDR']

    if not db.isAdmin(ip):
        return redirect('/')

    data = db.getUserList()
    banned = db.getBanList()
    return render_template('admin.html', data=data, banned=banned)


@app.route('/admin', methods=["POST"])
def ban_request():
    user = request.form['user']

    if ban_user(user):
        flash('Ban successful.','success')
        return redirect('/admin')
    else:
        flash('Ban failed.', 'danger')
        return redirect('/admin')



@app.route('/login', methods=["GET", "POST"])
def login_page():

    username = request.form['username']
    password = request.form['password']

    if db.isBanned(username):
        flash('User is banned.', 'danger')
        return redirect('/')

    if ipa.valid_login(username, password):
        admin_flag = ipa.isAdmin(username, password)

        ip = request.environ['REMOTE_ADDR']
        if not db.setUser(ip, username, admin_flag):
            flash('Database bind failed. Contact Drift.', 'danger')
            return redirect('/')

        # Allow the client IP address to access the internet
        ip_management.iptables_allow_ip(ip)

        return render_template("home.html")
    else:
        flash('Invalid username or password.', 'danger')
        return redirect('/')

@app.route('/')
def home():
    return render_template('login.html')


if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(host='0.0.0.0')
