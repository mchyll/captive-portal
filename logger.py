import logging
import logging.handlers
import sys


def setup_logger(*, log_level='INFO', syslog=True, stdout=False):
    log = logging.getLogger('captiveportal')
    log.setLevel(logging.getLevelName(log_level))

    if syslog:
        syslog_handler = logging.handlers.SysLogHandler(address='/dev/log')
        formatter = logging.Formatter('%(name)s: [%(levelname)s] %(message)s')
        syslog_handler.setFormatter(formatter)
        log.addHandler(syslog_handler)

    if stdout:
        stdout_hander = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter('%(asctime)s %(name)s: [%(levelname)s] %(message)s')
        stdout_hander.setFormatter(formatter)
        log.addHandler(stdout_hander)

    return log
