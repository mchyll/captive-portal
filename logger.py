#!/usr/bin/python
import logging
import logging.handlers
import sys

_logger = None


def _exception_logger(type, value, tb):
    _logger.exception('Uncaught exception: {}'.format(str(value)))


def get_logger(*, log_level='INFO', syslog=True, stdout=False):
    global _logger
    if not _logger:
        _logger = logging.getLogger('captiveportal')
        _logger.setLevel(logging.getLevelName(log_level))

        if syslog:
            syslog_handler = logging.handlers.SysLogHandler(address='/dev/log')
            formatter = logging.Formatter('%(name)s: [%(levelname)s] %(message)s')
            syslog_handler.setFormatter(formatter)
            _logger.addHandler(syslog_handler)

        if stdout:
            stdout_hander = logging.StreamHandler(sys.stdout)
            formatter = logging.Formatter('%(asctime)s %(name)s: [%(levelname)s] %(message)s')
            stdout_hander.setFormatter(formatter)
            _logger.addHandler(stdout_hander)

    sys.excepthook = _exception_logger

    return _logger
