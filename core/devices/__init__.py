"""Initialization Method."""
from core.devices.device import Device
from core.devices.android_device import AndroidDevice
from core.devices.ios_device import IOSDevice
from core.devices.device_factory import DeviceFactory

__all__ = ('Device', 'AndroidDevice', 'IOSDevice', 'DeviceFactory')
