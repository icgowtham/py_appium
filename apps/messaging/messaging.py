"""Class for all messaging related applications."""
from apps.base_app import BaseApp
# Import core modules
from core.devices.device import Device
from core.devices.device_factory import DeviceFactory
from core.logger import get_logger

LOGGER = get_logger().logger


class MessagingApp(BaseApp):
    """Class for all Messaging applications."""

    def __init__(self, app_name, device_type):
        """Initialization Method."""
        category = 'messaging'
        super().__init__(category, app_name.lower())
        self.main_device = DeviceFactory.get_device_type(device_type)(app_name, 'SERVER_1')
        self.second_device = DeviceFactory.get_device_type(device_type)(app_name, 'SERVER_2')
        if not (self.main_device.driver and self.second_device.driver):
            LOGGER.error('Two drivers are required!')
            raise Exception('Two drivers are required!')
        self.main_device.contact = self.config['CONTACT'][self.main_device.mobile_name]
        self.second_device.contact = self.config['CONTACT'][self.second_device.mobile_name]
        self.main_device.start_app()
        self.second_device.start_app()

    def perform_chat(self):
        """Perform chat using two mobiles on application."""

    def make_call_two_mobiles(self, duration):
        """Perform audio & video call using two mobiles on application."""

    def send_media_from_gallery(self):
        """Send photo & video from one mobile on application."""

    def send_instant_media(self, duration):
        """Send photo, audio & video from one mobile on application."""

    def share_files(self):
        """Send document / file from one mobile on application."""

    def put_status(self, duration):
        """Perform status update on application."""

    def all_features(self):
        """Run all automation features of application."""

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit method."""
        self.main_device.close_driver()
        self.second_device.close_driver()
        Device.stop_appium()
