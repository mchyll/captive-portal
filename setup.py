#!/usr/bin/python3
import sqlite3
from config import get_config
import subprocess
import os


if __name__ == '__main__':
    print('Warning: This will flush and reset any existing setup and data.')
    if input('Continue? [y/N] ').lower() == 'y':

        config = get_config()

        print('Flushing and setting up database schema')
        qry = open('create_db_tables.sql', 'r').read()
        conn = sqlite3.connect('user-ip.db')
        c = conn.cursor()
        c.executescript(qry)
        conn.commit()
        c.close()
        conn.close()

        print('Loading br_netfilter kernel module')
        subprocess.run(['modprobe', 'br_netfilter'], check=True)

        print('Flushing and setting up iptables rules')
        setup_iptables_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'setup_iptables')
        subprocess.run([setup_iptables_file, config['ip']], check=True)

        print('All done. Please restart the Captive Portal.')
