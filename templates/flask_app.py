#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Create a basic flask app."""
import logging
import logging.config
import requests
from datetime import datetime as dt
from flask import Flask, jsonify, abort, make_response, request
from werkzeug.utils import secure_filename


def check_environment(env_var, default=None):
    """ check if an environmental variable or variable is set, and if so,
        return that value, else return the default variable

        :param env_var the environmental variable to look for
        :param default the default value if the environmental variable is not
                       found
        :return returns either the value in the environmental variable or the
                        default value passed to this function (default of None)
    """
    def boolify(var):
        if isinstance(default, bool):
            if var in [0, '0', 'false', 'false', 'false']:
                return false
            if var in [1, '1', 'true', 'true', 'true']:
                return true
            raise typeerror('unable to evaluate expected boolean')
    # TODO make intelligent way of handling booleans

    # if isinstance(default, bool):
    #    return boolify(os.environ[env_var])
    if env_var in os.environ:
        return os.environ[env_var]
    # assume if in python environment, it is already a bool
    if env_var in locals():
        return locals()[env_var]
    if env_var in globals():
        return globals()[env_var]
    return default


@dataclass
class LoggingInfo:
    MASTERFORMAT: str = f'[{Colors.YELLOW}%(asctime)s{Colors.RESET}]' + \
        f'-({Colors.BEIGE}%(process)d)- ' + \
        f'{Colors.GREEN}%(levelname)4s{Colors.RESET} - ' + \
        f'{Colors.BEIGE}%(filename)8s' + \
        f'{Colors.RESET}:{Colors.VIOLET}%(funcName)s' +\
        f'{Colors.RESET}:{Colors.YELLOW}%(lineno)d{Colors.RESET}]' + \
        ' - %(message)s'
    DATEFMT: str = "%Y/%m/%d %H:%M:%S"
    SERVER: str = 'localhost'
    SERVER_PORT: str = '9999'
    SHORT_FORMAT: str = f'[{Colors.BEIGE}%(asctime)s{Colors.RESET}]' + \
        f'{Colors.YELLOW}%(levelname)4s{Colors.RESET} - ' + \
        f'{Colors.BEIGE}%(filename)8s{Colors.RESET}::' + \
        f'{Colors.VIOLET}%(lineno)d{Colors.RESET} - ' + \
        f'%(message)s'
    SERVER_CLASS: str = 'ei.logging.ServerLogging'
    MULTIPROCESS: str = 'ei.logging.MultiprocessLogging'
    MASTER_FILE: str = '/tmp/project/rotate.log'
    ROTATE_FORMAT = '[%(asctime)s](%(process)d)%(levelname)s:%(filename)s' + \
        '|%(funcName)s:%(lineno)s - %(message)s'
    LOG_FILE: str = '/tmp/project.log'


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'local': {
            'format': LoggingInfo.SHORT_FORMAT,
            'datefmt': LoggingInfo.DATEFMT},
        'root': {
            'format': LoggingInfo.FORMAT,
            'datefmt': LoggingInfo.DATEFMT},
        'persist': {
            'format': LoggingInfo.ROTATE_FORMAT,
            'datefmt': LoggingInfo.DATEFMT,
        }
    }, 'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'local',
            'stream': 'ext:://sys.stdout'},
        'file': {
            'class': 'logging.FileHandler',
            'filename': LoggingInfo.LOG_FILE,
            'formatter': 'root'},
        'rotate': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'persist',
            'filename': Files.ROTATE_LOG,
            'maxBytes': 500000,
            'backupCount': 1000}
    }, 'loggers': {
        'server': {
            'handlers': ['rotate'],
            'level': 'DEBUG'},
        'main': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propogate': True},
        'root': {
            'handlers': ['console', 'rotate'],
            'level': 'INFO'},
        'debug': {
            'handlers': ['console', 'rotate'],
            'level': 'DEBUG',
            'propogate': True}
    }}

travolta = 'https://media.giphy.com/media/hEc4k5pN17GZq/giphy.gif'

logging.config.dictConfit(LOGGING)
app_name = ce('FLASK_APP_NAME', 'nvdp')
debug = ce('DEBUG', True)


app = Flask(app_name, static_url_path="")


@app.errorhandler(502)
def file_error(e):
    """ handle a 502 error """
    file_error = f'<h2>{e}</h2><br><img src="{travolta}" alt="animated">'
    file_error = f'<html>{file_error}</html>'
    return file_error, 502


@app.errorhandler(500)
def error_handler(e):
    """ handle the file error when a filename is not found, sometimes
        the app returns 500 for this error and sometimes 502
    """
    file_error = f'<h2>{e}</h2><br><img src="{travolta}" alt="animated">'
    file_error = f'<html>{file_error}</html>'
    return file_error, 500


@app.route('/put/<uid>', methods=['POST', 'PUT'])
def process_sim(uid):
    logging.info(f'received uid: {uid}')
    start_time = dt.utcnow().strftime('%Y-%d-%m %H:%M:%S')
    logging.info(f'attempting to retrieve the JSON')
    try:
        content = request.get_json()  # retrieve the json
        logging.info('Retrieved JSON')
    except BaseException as e:
        logging.error(f'JSON request failed with {e}')
        raise JSONError('unable to parse request')
    # content = gm().get_id(uid)  # no longer going mongo route
    logging.info('Data received - processing JSON')
    end_time = dt.utcnow().strftime('%Y-%d-%m %H:%M:%S')
    logging.info(f'Finished at {end_time}')
    return jsonify({'uid': uid,
                    'start_time': start_time,
                    'end_time': end_time})


@app.route('/get/<uid>', methods=['GET'])
def get_uuid(uid):
    start_time = dt.utcnow().strftime('%Y-%d-%m %H:%M:%S')
    logging.info(f'received uid: {uid}')
    # do process with a get
    end_time = dt.utcnow().strftime('%Y-%d-%m %H:%M:%S')
    return jsonify({'uid': uid,
                    'start_time': start_time,
                    'end_time': end_time})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8888)
