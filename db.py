import os
import sqlite3


def getConnection():
    db_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'user-ip.db')
    db = sqlite3.connect(db_file)
    cursor = db.cursor()
    return cursor,db


def closeConnection(cursor,db):
    try:
        cursor.close()
        db.close()
        return True
    except:
        return False

#Checks if username is in list of banned users, returns True if user is banned
def isBanned(username):
    try:
        cursor,db = getConnection()
        cursor.execute("SELECT * FROM banned_users")
    except:
        closeConnection(cursor,db)
        return False

    for banned_user in cursor:
        banned_user = str(banned_user)[2:-3]

        if username == banned_user:
            closeConnection(cursor,db)
            return True

    closeConnection(cursor,db)
    return False
#Checks if IP is in list of admin users, returns True if user is admin
def isAdmin(ip):
    try:
        cursor,db = getConnection()
        cursor.execute('SELECT drifter FROM clients WHERE ip = ?', [ip])
    except:
        closeConnection(cursor,db)
        return False

    for drifter in cursor:
        drifter = str(drifter)[1:-2]
        if drifter == '1':
            closeConnection(cursor,db)
            return True

    closeConnection(cursor,db)
    return False

def setUser(ip, username, admin):
    try:
        cursor,db = getConnection()
        cursor.execute('INSERT INTO clients VALUES(?,?,?)', [str(ip), str(username), admin, int(''.join(ip.split('.')))])
        db.commit()
        closeConnection(cursor,db)
        return True
    except:
        closeConnection(cursor,db)
        return False

def getUserList():
    try:
        cursor,db = getConnection()
        cursor.execute("SELECT * FROM clients ORDER BY sort_number")
        data = cursor.fetchall()
        closeConnection(cursor,db)
        return data
    except:
        closeConnection(cursor,db)
        return False

def getBanList():
    try:
        cursor,db = getConnection()
        cursor.execute("SELECT * FROM banned_users")
        banned = cursor.fetchall()
        closeConnection(cursor,db)
        return banned
    except:
        closeConnection(cursor,db)
        return False




def banUser(username):
    try:
        cursor,db = getConnection()
        cursor.execute("SELECT ip FROM clients WHERE username = ?", [username])

        for ip in cursor.fetchall():
            ip = str(ip)[2:-3]
            cursor.execute('DELETE FROM clients WHERE ip = ?', [str(ip)])

        cursor.execute('INSERT INTO banned_users VALUES(?)', [username])
        db.commit()

        closeConnection(cursor,db)
        return True
    except:
        closeConnection(cursor,db)
        return False
