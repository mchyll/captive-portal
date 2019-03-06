#!/usr/bin/python
import json
from python_freeipa import Client, exceptions
from python_freeipa.exceptions import Unauthorized
from config import get_config

_config = get_config()


def valid_login(username, password):
    '''
    Tries to login and checks if user is member of admin-group

    :param username: user trying to log in
    :param password: user trying to log in
    :return: True on valid credentials, false on faliure
    '''
    try:
        client = Client(_config['ipa']['server'], verify_ssl=True, version=_config['ipa']['version'])
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
        client = Client(_config['ipa']['server'], verify_ssl=True, version=_config['ipa']['version'])
        client.login(username, password)
        var = client.group_find(_config['ipa']['admin_group'])
        return username in json.dumps(var)

    except Unauthorized:
        return False
