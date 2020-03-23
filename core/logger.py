# -*- coding: utf-8 -*-
"""Logger module."""
import datetime
import logging
import os
import sys

__all__ = ('Logger', 'get_logger')
_LOGGER_SINGLETON_INSTANCE = None
SUPPORTED_LEVELS_MAP = {
    'critical': logging.CRITICAL,
    'debug': logging.DEBUG,
    'error': logging.ERROR,
    'info': logging.INFO,
    'user': logging.ERROR,
    'warning': logging.WARNING
}


class Singleton(type):
    """Singleton meta-class."""

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """Override the call method."""
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class LogFormatter(logging.Formatter):
    """Custom log formatter."""

    def __init__(self):
        """Initialization method."""
        logging.Formatter.__init__(self)

    def format(self, record):
        """
        Override format method.

        :param record: object
            Log record object
        :return: str
            Formatted log message
        """
        timestamp = datetime.datetime.fromtimestamp(record.created).strftime('%Y-%m-%d %H:%M:%S')
        origin = '{fileName}#{lineNumber}'.format(
            fileName=record.filename,
            lineNumber=record.lineno)
        if record.funcName != '<module>':
            origin += ' ({functionName})'.format(functionName=record.funcName)
        return '[{ts: <19}]: {name}: {level: <8}: {msg: <68}: {origin}'.format(
            ts=timestamp,
            name=record.name,
            level=record.levelname,
            msg=record.getMessage(),
            origin=origin)


class Logger(metaclass=Singleton):
    """The log handling class."""

    def __init__(self, level=logging.DEBUG):
        """
        Initialization method for the logger.

        :param level: int
            Number to indicate the level of logging.
        """
        self._log_file_name = None
        self._timestamp = None
        self._logger = logging.getLogger('Android_Apps')
        # Work as a stand-alone logger when other loggers are not available.
        if not self._logger.handlers:
            handler = logging.StreamHandler()
            handler.setFormatter(LogFormatter())
            handler.setLevel(level)
            self._logger.addHandler(handler)
        # Disable duplicate logging. https://docs.python.org/3/library/logging.html#logger-objects
        self._logger.propagate = False
        self._logger.setLevel(logging.DEBUG)

    @property
    def logger(self):
        """Property getter for _logger."""
        return self._logger

    def start_file_logging(self, log_file_dir, log_level, app_name):
        """
        Method to start the file logging process.

        :param log_file_dir: str
            Path of the log file.
        :param log_level: str
            Logging level.
            Level Numeric value
                CRITICAL 50
                ERROR 40
                WARNING 30
                INFO 20
                DEBUG 10
        :param app_name: str
            Name of the application. For e.g. 'youtube'.
        :return: None
        """
        if log_level not in SUPPORTED_LEVELS_MAP:
            print('\nError: The log level specified is invalid.')
            print('Supported log levels are: <{lvl}>\n'.format(
                lvl='|'.join(list(SUPPORTED_LEVELS_MAP.keys()))))
            sys.exit(1)

        has_file_handler = False

        for handler in self._logger.handlers:
            if isinstance(handler, logging.FileHandler):
                has_file_handler = True
                break
        if not has_file_handler:
            self._timestamp = datetime.datetime.now().strftime('%d_%m_%y_%H_%M_%S')
            log_file_name = 'logs_' + app_name + '_' + self._timestamp + '.log'
            self._log_file_name = os.path.join(log_file_dir, log_file_name)
            file_handler = logging.FileHandler(self._log_file_name)
            file_handler.setFormatter(LogFormatter())
            file_handler.setLevel(SUPPORTED_LEVELS_MAP[log_level])
            self._logger.addHandler(file_handler)
        self._logger.setLevel(SUPPORTED_LEVELS_MAP[log_level])

    def get_log_file_name(self):
        """Method to return the name of the log file."""
        return self._log_file_name


def get_logger(level=logging.DEBUG):
    """
    Function to return the logger object handle.

    :param: None
    :return: object
        The logger handle object.
    """
    global _LOGGER_SINGLETON_INSTANCE  # pylint: disable=global-statement
    if _LOGGER_SINGLETON_INSTANCE is None:
        _LOGGER_SINGLETON_INSTANCE = Logger(level)
    return _LOGGER_SINGLETON_INSTANCE
