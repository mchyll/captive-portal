#!/usr/bin/python
import logging
import logging.handlers
import sys

_logger = None


def setup_logger(*, name='captiveportal', log_level='INFO', syslog=True, stdout=False):
    global _logger
    if not _logger:
        _logger = logging.getLogger(name)
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

    return _logger
