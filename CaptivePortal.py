#!/usr/bin/python
import logging
import functools
from config import get_config
from flask import Flask, render_template, request, flash, redirect, abort
import os
import ipa_auth as ipa
import db
import ip_management

app = Flask(__name__)
log = logging.getLogger('captiveportal')
config = get_config()


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
        if not ip_management.iptables_disallow_ip(ip):
            return False

    return db.banUser(user)


def require_admin(endpoint):
    @functools.wraps(endpoint)
    def wrapper(*args, **kwargs):
        ip = get_client_ip()
        if not db.isAdmin(ip):
            log.warning('Client {} tried to access admin endpoint {} but is not drifter'.format(ip, request.url_rule))
            return abort(status=403)
        return endpoint(*args, **kwargs)

    return wrapper


@app.route('/admin', methods=["GET"])
@require_admin
def admin_page():
    data = db.getUserList()
    banned = db.getBanList()
    return render_template('admin.html', data=data, banned=banned)


@app.route('/admin/ban', methods=["POST"])
@require_admin
def ban_request():
    user = request.form['user']

    if ban_user(user):
        log.info('Banned user {}'.format(user))
        flash('Ban successful.', 'success')

    else:
        log.error('Banning of user {} failed'.format(user))
        flash('Ban failed.', 'danger')

    return redirect('/admin', code=303)


@app.route('/admin/unban', methods=['POST'])
@require_admin
def unban_request():
    user = request.form['user']

    if db.unbanUser(user):
        log.info('Unbanned user {}'.format(user))
        flash('Unban successful.', 'success')

    else:
        log.error('Unbanning of user {} failed'.format(user))
        flash('Unban failed.', 'danger')

    return redirect('/admin', code=303)


@app.route('/login', methods=['POST'])
def login_page():

    username = request.form['username']
    password = request.form['password']

    if db.isBanned(username):
        log.warning('Banned user {} tried to log in'.format(username))
        flash('User is banned.', 'danger')

    elif ipa.valid_login(username, password):
        ip = get_client_ip()
        admin_flag = ipa.isAdmin(username, password)

        # Add the client IP and username to the database
        if db.setUser(ip, username, admin_flag):

            # Allow the client IP address to access the internet
            if ip_management.iptables_allow_ip(ip):
                log.info('User {} (ip {}) authorized and allowed internet access'.format(username, ip))

            else:
                log.error('Iptables error when trying to allow client (user {}, ip {})'.format(username, ip))
                flash('En feil oppstod når vi prøvde å gi deg internettilgang. Ta kontakt med Drift.', 'danger')
                # Roll back the database entry on error
                db.removeIpEntry(ip)

        else:
            log.error('Database error when trying to add user to clients table (user {}, ip {})'.format(username, ip))
            flash('En databasefeil oppstod. Ta kontakt med Drift.', 'danger')

    else:
        log.warning('Invalid credentials for user {}'.format(username))
        flash('Feil brukernavn eller passord.', 'danger')

    return redirect('/', code=303)


@app.route('/', methods=['GET'], defaults={'path': ''})
@app.route('/<path:path>', methods=['GET'])
def home(path):
    authenticated_users = [ip[0] for ip in db.getUserList()]
    if get_client_ip() in authenticated_users:
        return render_template('home.html')
    else:
        return render_template('login.html')


if __name__ == "__main__":
    import logger
    logger.setup_logger(syslog=config['log']['syslog'],
                        stdout=config['log']['stdout'],
                        log_level=config['log']['level'])

    log.info('Flask application starting')
    app.secret_key = os.urandom(12)
    app.run(host='0.0.0.0', port=config['flask_port'])
