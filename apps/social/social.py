"""Class for all social related applications."""
import sys

from apps.base_app import BaseApp
# Import core modules
from core.devices.device import Device
from core.devices.device_factory import DeviceFactory
from core.logger import get_logger

LOGGER = get_logger().logger


class SocialApp(BaseApp):
    """Class for all Social applications."""

    def __init__(self, app_name, device_type):
        """Initialization Method."""
        category = 'social'
        super().__init__(category, app_name.lower())
        self.main_device = DeviceFactory.get_device_type(device_type)(app_name, 'SERVER_1')
        if not self.main_device.driver:
            LOGGER.error('Driver was not created! Exiting now!')
            sys.exit(1)
        self.main_device.start_app()

    def watch_videos(self, duration):
        """Watch videos on the applications."""

    def check_in(self):
        """Perform check-in of your location."""

    def gallery_media_upload(self):
        """Select photo & video from gallery & upload."""

    def instant_media_upload(self, duration):
        """Click a picture & capture video live & upload."""

    def like_comment_share(self):
        """Perform like, comment & share."""

    def send_friend_request(self):
        """Send friend request."""

    def all_features(self):
        """Run all automation features of application."""

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit method."""
        self.main_device.close_driver()
        Device.stop_appium()
