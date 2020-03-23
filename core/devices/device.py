"""Base class for Device."""
import os
import sys
import subprocess
from abc import ABCMeta, abstractmethod

import yaml

from core.logger import get_logger

LOGGER = get_logger().logger


def read_config_file(config_file):
    """
    Read YAML file and return dictionary with values.

    :param config_file: str
        Name of YAML file to be read.
    :return: dict
        Configuration dictionary created after reading YAML file
    """
    try:
        with open(config_file) as stream:
            config_dict = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        LOGGER.error('Encountered some ERROR while trying to load {fl}'.format(fl=config_file))
        LOGGER.error(str(exc))
        sys.exit(1)
    return config_dict


class Device(metaclass=ABCMeta):
    """Class containing all methods relating to driver."""

    def __init__(self, app_name):
        """Initialization Method."""
        self.x_cord = None
        self.start_y = None
        self.end_y = None
        self.app_name = app_name
        self.config = read_config_file(os.path.join(os.environ['basedir'],
                                                    'core',
                                                    'devices',
                                                    'appium_server_config.yaml'))

    @abstractmethod
    def create_driver(self, app_server):
        """Create a driver to the specified appium server & return driver,touch objects."""

    @abstractmethod
    def close_driver(self):
        """Close the application, quits the drivers."""

    @abstractmethod
    def set_scroll_length(self):
        """Read mobile window size & sets the scroll length for a mobile."""

    @abstractmethod
    def tap_screen(self, element=None, config=None, x_cord=None, y_cord=None):
        """Perform tap for requested element or coordinates."""

    @abstractmethod
    def swipe_up(self):
        """Swipe the screen to scroll down."""

    @abstractmethod
    def swipe_right(self, config):
        """Swipe the screen to move right."""

    @abstractmethod
    def press_long(self, hold_time, element=None, config=None, x_cord=None, y_cord=None):
        """Method to perform long press of element or a coordinate."""

    @abstractmethod
    def press_long_and_slide(self, element, x_cord, y_cord, hold_time):
        """Method to perform long press of element or a coordinate."""

    @abstractmethod
    def return_element(self, el_type, text, bounds=False):
        """Return element according to element type given."""

    @abstractmethod
    def return_button(self, text, class_name='android.widget.TextView'):
        """Return element matching the text which is passed to it."""

    @abstractmethod
    def click_element(self, el_type, text, delay, handle_error):
        """Search for element using accessibility id or xpath and click it."""

    @abstractmethod
    def press_back(self, num=1):
        """Press back button on mobile for 'num' times."""

    @abstractmethod
    def click_using_class(self, text, search_text, delay=3, is_button=False):
        """Return element according to 'text' or 'search text' and clicks it."""

    @abstractmethod
    def start_app(self):
        """Open the application on the mobile device."""

    @staticmethod
    def stop_appium():
        """Kill appium servers running on Windows using Powershell."""
        subprocess.run('powershell Stop-Process -name node', shell=True,
                       stderr=subprocess.STDOUT, check=False)
        LOGGER.info("Appium server killed!")
