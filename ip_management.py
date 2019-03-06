#!/usr/bin/python
import subprocess
import logging

_log = logging.getLogger('captiveportal')


def iptables_allow_ip(ip):
    """
    Allows an IP address to access the internet by adding the necessary rules in iptables.

    :param ip: the IP address to allow internet access
    :return: True if the iptables commands exited successfully, False otherwise
    """
    try:
        subprocess.run(['iptables', '-t', 'nat', '-I', 'PREROUTING', '-s', ip, '-j', 'ACCEPT'], check=True)
        subprocess.run(['iptables', '-I', 'FORWARD', '-s', ip, '-j', 'ACCEPT'], check=True)
        subprocess.run(['iptables', '-I', 'FORWARD', '-d', ip, '-j', 'ACCEPT'], check=True)

        return True

    except:
        _log.exception('Exception on allowing user internet access')
        return False


def iptables_disallow_ip(ip):
    """
    Disallows an IP address to access the internet by removing the associated rules in iptables.

    :param ip: the IP address to disallow internet access
    :return: True if the iptables commands exited successfully, False otherwise
    """
    try:
        subprocess.run(['iptables', '-t', 'nat', '-D', 'PREROUTING', '-s', ip, '-j', 'ACCEPT'], check=True)
        subprocess.run(['iptables', '-D', 'FORWARD', '-s', ip, '-j', 'ACCEPT'], check=True)
        subprocess.run(['iptables', '-D', 'FORWARD', '-d', ip, '-j', 'ACCEPT'], check=True)

        return True

    except:
        _log.exception('Exception on disallowing user internet access')
        return False
