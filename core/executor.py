"""Executor class."""
import os
import sys
from importlib import import_module

# Import core modules
from core.devices.device import read_config_file
from core.logger import get_logger

__all__ = ('Executor',)
LOGGER = get_logger().logger


class Executor:
    """Executor Class."""

    def __init__(self, cmd_args):
        """Initialization Method."""
        config_path = os.path.join(os.environ['basedir'], 'core', 'app_categories.yaml')
        self.apps_config = read_config_file(config_path)
        self.app_name = cmd_args['app'].lower()
        self.category = self.get_app_category(self.app_name)
        self.device_type = cmd_args['device_type'].lower()

    def get_app_category(self, app_name):
        """
        Search app name in YAML file and returns the category.

        :param app_name: str
            Name of application
        :return: str
            Category of application if found. (Example: 'social', 'streaming', 'messaging')
        """
        for category in self.apps_config:
            if app_name in self.apps_config[category]:
                LOGGER.info('Category for {app} is identified as: {cate}'.format(
                    app=app_name, cate=category))
                return category
        try:
            raise TypeError
        except TypeError:
            LOGGER.error('Category for {app} cannot be identified!'.format(app=app_name))
            sys.exit(1)

    def execute_automation(self):
        """
        Method to execute mobile automation.

        :return: None
        """
        sys.path.append(os.path.sep.join([os.environ['basedir'], 'apps', self.category, self.app_name]))
        test_module = import_module('.'.join(['apps', self.category, self.app_name, self.app_name]))
        class_name = next(vars(test_module)[k] for k in vars(test_module)
                          if k.lower() == self.app_name)
        if class_name:
            LOGGER.debug('Found class {ap}!'.format(ap=class_name))
            LOGGER.critical('########## Running Automation for '
                            '{app} ##########'.format(app=self.app_name))
            # Create class object & call all app features.
            with class_name(self.device_type) as app_obj:
                app_obj.all_features()
            LOGGER.info('Automation execution completed.')
        else:
            LOGGER.error('Cannot find class name for {app}'.format(app=self.app_name))
            sys.exit(1)
