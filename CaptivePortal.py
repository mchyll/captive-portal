#!/usr/bin/python
from flask import Flask, render_template, request, flash, redirect, abort
import os
import ipa_auth as ipa
import db
import ip_management
import logger

app = Flask(__name__)

# TODO: change this to defaults (syslog=True, stdout=False) in prod
log = logger.get_logger(syslog=False, stdout=True, log_level='DEBUG')


def get_client_ip():
    try:
        return request.headers['X-Real-IP']
    except KeyError:
        ip = request.environ['REMOTE_ADDR']
        log.debug('No X-Real-IP header, using REMOTE_ADDR: {} (not behind nginx proxy?)'.format(ip))
        return ip


def ban_user(user):
    # Disallow internet access for all IPs associated with the user
    for ip in db.getIPsForUser(user):
        ip_management.iptables_disallow_ip(ip)

    if db.banUser(user):
        return True

    return False


@app.route('/admin', methods=["GET"])
def admin_page():

    ip = get_client_ip()

    if not db.isAdmin(ip):
        log.warning('Client {} tried to access admin page but is not drifter'.format(ip))
        return redirect('/')

    data = db.getUserList()
    banned = db.getBanList()
    return render_template('admin.html', data=data, banned=banned)


@app.route('/admin', methods=["POST"])
def ban_request():
    user = request.form['user']
    ip = get_client_ip()

    if not db.isAdmin(ip):
        log.warning('Client {} tried to ban user {} but is not drifter'.format(ip, user))
        return abort(status=403)

    if ban_user(user):
        log.info('Banned user {}'.format(user))
        flash('Ban successful.', 'success')
        return redirect('/admin')
    else:
        log.error('Banning of user {} failed'.format(user))
        flash('Ban failed.', 'danger')
        return redirect('/admin')


@app.route('/login', methods=["POST"])
def login_page():

    username = request.form['username']
    password = request.form['password']

    if db.isBanned(username):
        log.warning('Banned user {} tried to log in'.format(username))
        flash('User is banned.', 'danger')
        return redirect('/')

    if ipa.valid_login(username, password):
        admin_flag = ipa.isAdmin(username, password)

        ip = get_client_ip()
        if not db.setUser(ip, username, admin_flag):
            log.error('Database error when trying to add user to clients table (user {}, ip {})'.format(username, ip))
            flash('Database bind failed. Contact Drift.', 'danger')
            return redirect('/')

        # Allow the client IP address to access the internet
        if not ip_management.iptables_allow_ip(ip):
            log.error('Iptables error when trying to allow client (user {}, ip {})'.format(username, ip))
            flash('An error occurred when trying to give you internet access. Contact Drift.', 'danger')
            return redirect('/')

        log.info('User {} (ip {}) authorized and allowed internet access'.format(username, ip))
        return render_template("home.html")
    else:
        log.warning('Invalid credentials for user {}'.format(username))
        flash('Invalid username or password.', 'danger')
        return redirect('/')


@app.route('/')
def home():
    return render_template('login.html')


if __name__ == "__main__":
    log.info('Flask application starting')
    app.secret_key = os.urandom(12)
    app.run(host='0.0.0.0')
