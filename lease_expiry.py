#!/usr/bin/python
import os
import sqlite3
import sys


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Please supply the IP address of the expired lease.')
        exit(1)

    db_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'user-ip.db')
    db = sqlite3.connect(db_file)
    cursor = db.cursor()

    ip_to_remove = sys.argv[1]
    cursor.execute('DELETE FROM clients WHERE ip = ?', [ip_to_remove])
    db.commit()

    exit_code = 0
    if cursor.rowcount < 1:
        exit_code = 1

    cursor.close()
    db.close()

    exit(exit_code)
