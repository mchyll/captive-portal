from flask import Flask, render_template, request, flash, redirect
import sqlite3
import os
import ipa_auth as ipa
import db


app = Flask(__name__)



def ban_user(user):

    # TODO: remove form IPTABLES, and release IP in DHCP

    db.banUser(user)



@app.route('/admin', methods=["GET"])
def admin_page():

    # TODO: get requesting IP

    ip = "192.168.1.3"  # Admin
    #ip = "192.168.1.13"  # bruker

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

        # TODO: get IP from request
        ip = 'testIP'
        if not db.setUser(ip, username, password):
            flash('Database bind failed. Contact Drift.', 'danger')
            return redirect('/')

        # TODO: add IP to iptables


        return render_template("home.html")
    else:
        flash('Invalid username or password.', 'danger')
        return redirect('/')

@app.route('/')
def home():
    print('incoming IP: ',request.environ['REMOTE_ADDR'])
    return render_template('login.html')


if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(host='0.0.0.0')
