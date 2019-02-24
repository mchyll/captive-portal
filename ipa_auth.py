import json
from python_freeipa import Client, exceptions
from python_freeipa.exceptions import Unauthorized

ipa_server = 'ipa.demo1.freeipa.org'
#ipa_server = 'ipa1.tihlde.org'
ipa_version = '2.215'
#admin_group = 'drift'
admin_group = 'admins'

def get_admin_group():
    return admin_group

#Tries to login and checks if user is member of admin-group
def ipa_login(username, password):
    try:
        client = Client(ipa_server, verify_ssl=True, version=ipa_version)
        client.login(username, password)
        return True
    except Unauthorized:
        return False

#Checks if user is member of admin-group
def isAdmin(username, password):
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
