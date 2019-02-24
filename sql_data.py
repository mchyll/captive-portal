#!/usr/bin/python
import os
import sqlite3
import sys


if __name__ == '__main__':
    db_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'user-ip.db')
    db = sqlite3.connect(db_file)
    cursor = db.cursor()

    cursor.execute('DROP TABLE IF EXISTS clients')
    cursor.execute('DROP TABLE IF EXISTS banned_users')
    cursor.execute('CREATE TABLE clients (ip TEXT PRIMARY KEY,username TEXT NOT NULL,drifter INTEGER NOT NULL DEFAULT 0)')
    cursor.execute('CREATE TABLE banned_users (username TEXT NOT NULL)')
    db.commit()

    for i in range(1,10):
        cursor.execute('INSERT INTO clients VALUES(?,?,?)', ["192.168.1."+str(i), "Bruker"+str(i), True])

    for i in range(11,19):
        cursor.execute('INSERT INTO clients VALUES(?,?,?)', ["192.168.1."+str(i), "Bruker"+str(i), False])

    cursor.execute('INSERT INTO clients VALUES(?,?,?)', ["192.168.1.40", "Bruker5", True])
    db.commit()

    for i in range(20, 25):
        cursor.execute('INSERT INTO banned_users VALUES(?)', ["Bruker"+str(i)])
    db.commit()




    cursor.close()
    db.close()
