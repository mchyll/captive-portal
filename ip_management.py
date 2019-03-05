#!/usr/bin/python
import subprocess


def iptables_allow_ip(ip):
    """
    Allows an IP address to access the internet by adding the necessary rules in iptables.

    :param ip: the IP address to allow internet access
    :return: True if the iptables commands exited successfully, False otherwise
    """
    try:
        subprocess.run(['iptables', '-t', 'nat', '-I', 'PREROUTING', '-s', ip, '-j', 'ACCEPT'], shell=True, check=True)
        subprocess.run(['iptables', '-I', 'FORWARD', '-s', ip, '-j', 'ACCEPT'], shell=True, check=True)
        subprocess.run(['iptables', '-I', 'FORWARD', '-d', ip, '-j', 'ACCEPT'], shell=True, check=True)

        return True

    except subprocess.CalledProcessError:
        return False


def iptables_disallow_ip(ip):
    """
    Disallows an IP address to access the internet by removing the associated rules in iptables.

    :param ip: the IP address to disallow internet access
    :return: True if the iptables commands exited successfully, False otherwise
    """
    try:
        subprocess.run(['iptables', '-t', 'nat', '-D', 'PREROUTING', '-s', ip, '-j', 'ACCEPT'], shell=True, check=True)
        subprocess.run(['iptables', '-D', 'FORWARD', '-s', ip, '-j', 'ACCEPT'], shell=True, check=True)
        subprocess.run(['iptables', '-D', 'FORWARD', '-d', ip, '-j', 'ACCEPT'], shell=True, check=True)

        return True

    except subprocess.CalledProcessError:
        return False
