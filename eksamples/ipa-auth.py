from python_freeipa import Client, exceptions

ipa_server = 'ipa.demo1.freeipa.org'
ipa_version = '2.215'
uname = 'test3'     #Username to authenticate
pwd = 'testtest123'     #Users password default: testtest123

def login_check(uname, pwd):
    try:
        userClient = Client(ipa_server, version=ipa_version)
        userClient.login(uname, pwd)
        return True
    except exceptions.Unauthorized:
        return False

if login_check(uname, pwd):
    print("Innlogging godkjent")
else:
    print("Innlogging feilet")
