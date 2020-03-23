# -*- coding: utf-8 -*-
"""
run.py - script to launch a regression.

With this script user can provide option to run mobile automation.
Only --app argument is mandatory and few are optional to start the regression.

Usage:
python run.py --app whatsapp
"""
import argparse
import getpass
import os
import sys

# import core modules
from core.executor import Executor
from core.logger import get_logger, Logger

LOGGER = get_logger().logger
LOG_FILE_BASE_DIR = None


def start_logging(log_level, app_name):
    """
    Function to start the logging for the testing.

    :param log_level: str
         'user', 'info', 'debug'. verbosity level: 'debug' > 'info' > 'user'
    :param app_name: str
        Name of the application.
    :return: None
    """
    lgr = Logger()
    log_file_dir = os.path.join(LOG_FILE_BASE_DIR, getpass.getuser())
    if not os.path.exists(log_file_dir):
        try:
            os.makedirs(log_file_dir)
        except OSError as exp:
            print('ERROR: Could not create log file directory'
                  'to store regression logs: ' + str(exp))
            print(sys.exc_info())
    lgr.start_file_logging(log_file_dir, log_level, app_name)


def parse_cmd_line_arguments():
    """
    Function to parse the command line arguments passed by the user.

    :param: None
    :return: dict
    """
    parser = argparse.ArgumentParser(
        description='''
        {nm} script to launch a regression.\n
        For e.g.: python {nm} --app youtube
        '''.format(nm=sys.argv[0]))
    parser.add_argument('--app', help='Name of the app to run.',
                        required=True)
    parser.add_argument('--device-type',
                        required=False,
                        default='android',
                        help='<android|ios> Type of device.')
    parser.add_argument('--log-level',
                        required=False,
                        default='debug',
                        help='<user|info|debug> Increasing verbosity order user<info<debug.')
    parser.add_argument('--log-file-dir',
                        required=False,
                        default=None,
                        help='The directory to store the log files.')
    return vars(parser.parse_args())


if __name__ == '__main__':
    assert sys.version_info >= (3, 5), 'This application requires Python 3.5 or higher to run.'

    # Base directory of the application.
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    os.environ['basedir'] = BASE_DIR
    LOGGER.info('Base dir: {dir}'.format(dir=BASE_DIR))

    # Add 'core' folder to sys path.
    sys.path.append(BASE_DIR + 'core')
    sys.path.append(BASE_DIR + 'apps')

    # Get user arguments.
    ARGS = parse_cmd_line_arguments()
    if not ARGS['log_file_dir']:
        LOG_FILE_BASE_DIR = 'C:\\Temp\\MobileAppsFramework\\logs'
        ARGS['log_file_dir'] = LOG_FILE_BASE_DIR
    else:
        LOG_FILE_BASE_DIR = ARGS['log_file_dir']
    start_logging(ARGS['log_level'], ARGS['app'].lower())

    CMD = 'python {nm} '.format(nm=sys.argv[0])
    for key, value in ARGS.items():
        if value:
            CMD += '--' + str(key) + ' ' + str(value) + ' '
    HASH_STR = '##############################'
    LOGGER.critical('{ha} Executing Mobile Automation with command {ha}'
                    '\n{cmd}'.format(cmd=CMD, ha=HASH_STR))
    LOGGER.info('{ha}{ha}{ha}'.format(ha=HASH_STR))

    executor = Executor(ARGS)
    executor.execute_automation()
