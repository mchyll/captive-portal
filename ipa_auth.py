import json
from python_freeipa import Client, exceptions
from python_freeipa.exceptions import Unauthorized

ipa_version = '2.215'

# Single point of change
prod = False

if prod = True:
    ipa_server = 'ipa1.tihlde.org'
    admin_group = 'drift'
else:
    ipa_server = 'ipa.demo1.freeipa.org'
    admin_group = 'admins'


def valid_login(username, password):
    '''
    Tries to login and checks if user is member of admin-group

    :param username: user trying to log in
    :param password: user trying to log in
    :return: True on valid credentials, false on faliure
    '''
    try:
        client = Client(ipa_server, verify_ssl=True, version=ipa_version)
        client.login(username, password)
        return True
    except Unauthorized:
        return False


def isAdmin(username, password):
    '''
    Checks if user is member of admin-group.

    :param username: of the user to the checked
    :param password: of the user to the checked
    :return: True if admin, false otherwise
    '''
    try:
        client = Client(ipa_server, verify_ssl=True, version=ipa_version)
        client.login(username, password)
        var = client.group_find(admin_group)
        if username in json.dumps(var):
            return True
        else:
            return False

    except Unauthorized:
        return False
