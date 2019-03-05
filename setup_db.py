#!/usr/bin/python3
import sqlite3


qry = open('create_db_tables.sql', 'r').read()
conn = sqlite3.connect('user-ip.db')
c = conn.cursor()
c.executescript(qry)
conn.commit()
c.close()
conn.close()
print('Database setup finished')
