import os
import sys
import datetime
import inspect
import logging
from logging import DEBUG, WARNING, CRITICAL, ERROR, INFO
from logging.handlers import RotatingFileHandler
import constant_strings
import json
from imp import reload


LOG_TYPE_REVERSE_ENUM = {
    'DEBUG': DEBUG,
    'WARNING': WARNING,
    'CRITICAL': CRITICAL,
    'ERROR': ERROR,
    'INFO': INFO
}

LOG_FILE_PATH = os.environ.get('LOG_FILE_PATH', 'service.log')
LOG_LEVEL = LOG_TYPE_REVERSE_ENUM[os.environ.get('LOG_LEVEL', 'INFO')]

rotatingHandler = RotatingFileHandler(filename=LOG_FILE_PATH,
                                      maxBytes=20000,
                                      backupCount=1)


logging_params = {
    'level': LOG_LEVEL,
    'format': '%(message)s',
    'datefmt': '%Y-%m-%dT%H:%M:%S%z',
    'handlers': [rotatingHandler]
}


def init_logger():
    reload(logging)
    logging.basicConfig(**logging_params)
    logging.getLogger().setLevel(logging.INFO)


def get_standard_log(message, level, run_hash, service_name):
    """
    Returns a dict containing a standard log message.
    """
    stamp = datetime.datetime.utcnow().isoformat(timespec='milliseconds') + 'Z'
    msgDict = {
        'message': message,
        'timestamp': stamp,
        'run_hash': run_hash,
        'level': level,
        'service': service_name}
    return msgDict


def log(message, run_hash, msg_loglevel, service_name, loglevel):
    message = get_standard_log(message, msg_loglevel, run_hash, service_name)
    message = json.dumps(message)
    logging.log(loglevel, f'{message}')
    if (loglevel >= LOG_LEVEL):
        print(message, flush=True)


def debug(message, run_hash=None, service_name=None):
    log(message, run_hash, constant_strings.LEVEL_DEBUG, service_name, DEBUG)


def warning(message, run_hash=None, service_name=None):
    log(message, run_hash, constant_strings.LEVEL_WARN, service_name, WARNING)


def critical(message, run_hash=None, service_name=None):
    log(message, run_hash, constant_strings.LEVEL_CRIT, service_name, CRITICAL)


def error(message, run_hash=None, service_name=None):
    log(message, run_hash, constant_strings.LEVEL_ERROR, service_name, ERROR)


def info(message, run_hash=None, service_name=None):
    log(message, run_hash, constant_strings.LEVEL_INFO, service_name, INFO)
