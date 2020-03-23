"""Class for all streaming related applications."""
import sys

from apps.base_app import BaseApp
# Import core modules
from core.devices.device import Device
from core.devices.device_factory import DeviceFactory
from core.logger import get_logger

LOGGER = get_logger().logger


class StreamingApp(BaseApp):
    """Class for all Streaming applications."""

    def __init__(self, app_name, device_type):
        """Initialization Method."""
        category = 'streaming'
        super().__init__(category, app_name.lower())
        self.main_device = DeviceFactory.get_device_type(device_type)(app_name, 'SERVER_1')
        if not self.main_device.driver:
            LOGGER.error('Driver was not created! Exiting now!')
            sys.exit(1)
        self.main_device.start_app()

    def watch_videos(self, num_vid, duration=10):
        """Watch videos on application."""

    def upload_video(self, duration):
        """Upload video on application."""

    def share_download_save(self):
        """Share, download & save video on application."""

    def all_features(self):
        """Run all automation features of application."""

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit method."""
        self.main_device.close_driver()
        Device.stop_appium()
