import yaml
import logging

_config = None
_log = logging.getLogger('captiveportal')


def get_config():
    global _config

    if _config is None:
        _log.debug('Loading config from file')

        with open('config.yml') as file:
            _config = yaml.load(file)

    return _config
