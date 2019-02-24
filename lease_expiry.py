#!/usr/bin/python
import os
import sqlite3
import sys
import ip_management

"""
This script removes an IP address from the database and its iptables rules when its dhcp lease expires.
It is only meant to be run automatically by isc-dhcp-server on the lease expiry event.
"""

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Please supply the IP address of the expired lease.')
        sys.exit(1)

    ip_to_remove = sys.argv[1]
    exit_code = 0

    # Disallow internet access for the IP address
    if not ip_management.iptables_disallow_ip(ip_to_remove):
        exit_code = 1

    db_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'user-ip.db')
    db = sqlite3.connect(db_file)
    cursor = db.cursor()

    # Delete the database entry for the IP
    cursor.execute('DELETE FROM clients WHERE ip = ?', [ip_to_remove])
    db.commit()

    if cursor.rowcount < 1:
        exit_code = 1

    cursor.close()
    db.close()

    sys.exit(exit_code)
