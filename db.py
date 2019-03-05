#!/usr/bin/python
import os
import sqlite3


def getConnection():
    '''
    Generates a connection to the database file we use to store the ip-user connection

    :return: the cursor and the connection
    '''
    db_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'user-ip.db')
    db = sqlite3.connect(db_file)
    cursor = db.cursor()
    return cursor,db


def closeConnection(cursor,db):
    '''
    Closes the connection given by getConnection. remember to call this before
    every return-statement in the functions that uses it.

    :param cursor: The database cursor given by getConnection
    :param db: Connection to the database given by getConnection
    :return: True on success, false on failure
    '''
    try:
        cursor.close()
        db.close()
        return True
    except:
        return False


def isBanned(username):
    '''
    Checks if username is in list of banned users, returns True if user is banned.

    :param username: username of the user to be banned
    :return: True if user is banned
    '''
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


def isAdmin(ip):
    '''
    Checks if IP is in list of admin users, returns True if user is admin.

    :param ip: ip to be checked, usually the requesting ip
    :return: true if the ip is bound to an admin in the database table clients
    '''
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
    '''
    Innserts a user to the database table cliets upton login

    :param ip: to the one trying to log in
    :param username: given in the login field
    :param amdin: a flag true/fasle or 1/0 to be stored in the cliets table
    :return: true on success
    '''
    try:
        cursor,db = getConnection()
        cursor.execute('INSERT INTO clients VALUES(?,?,?,?)', [str(ip), str(username), admin, int(''.join(ip.split('.')))])
        db.commit()
        closeConnection(cursor,db)
        return True
    except:
        closeConnection(cursor,db)
        return False

def getUserList():
    '''
    Generates a list of IPs and users connected to them

    :return: a list of users, false on failure
    '''
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
    '''
    Generates a list of banned users from the 'banned_users' table in the Database

    :return: a list of banned users, false on failure
    '''
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
    '''
    Deletes all rows with ip of the given user from the clients table, and Innserts
    into bannes_users table

    :param username: of the user you want to ban
    :return: tru on success, false on failure
    '''
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


def getIPsForUser(username):
    """
    Returns all the IP adresses associated with a user. Returns an empty list
    if no IPs were found, or if a database error occured.

    :param username: the username to find IPs for
    :return: a list of IPs, or an empty list if no IPs were found or a database error occured.
    """

    cursor = None
    db = None
    try:
        cursor, db = getConnection()
        cursor.execute('SELECT ip FROM clients WHERE username = ?', [username])
        data = cursor.fetchall()

        return [row[0] for row in data]

    except:
        return []

    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()
