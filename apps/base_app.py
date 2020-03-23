"""Base app class for android applications."""
import os
from abc import ABCMeta, abstractmethod

# import core modules
from core.devices.device import read_config_file
from core.logger import get_logger

LOGGER = get_logger().logger


class BaseApp(metaclass=ABCMeta):
    """Base App Class."""

    def __enter__(self):
        """Setup Method."""
        return self

    def __init__(self, category_name, app_name):
        """Initialization Method."""
        self.category_name = category_name
        self.app_name = app_name
        self.config_path = os.path.join(os.environ['basedir'],
                                        'apps',
                                        self.category_name,
                                        self.app_name,
                                        'config',
                                        'app_config.yaml')
        self.config = read_config_file(self.config_path)

    @abstractmethod
    def all_features(self):
        """Method that contains all automation features for applications."""

    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit method."""
