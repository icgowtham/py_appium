""""Device Factory class."""
from core.devices.android_device import AndroidDevice
from core.devices.ios_device import IOSDevice


# pylint: disable=too-few-public-methods
class DeviceFactory:
    """Device Factory Class."""

    @staticmethod
    def get_device_type(device_type):
        """Identify type of device and returns the appropriate class."""
        if device_type == 'android':
            return AndroidDevice
        if device_type == 'ios':
            return IOSDevice
        raise NotImplementedError('Device type {dt} is currently not supported!'.format(
            dt=device_type))
