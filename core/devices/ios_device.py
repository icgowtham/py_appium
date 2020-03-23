"""IoS Device class for performing actions on ios apps."""
from core.devices.device import Device


class IOSDevice(Device):
    """IOS Device Class."""

    def create_driver(self, app_server):
        """Create a driver to the specified appium server & return driver,touch objects."""

    def close_driver(self):
        """Close the application, quits the drivers."""

    def set_scroll_length(self):
        """Read mobile window size & sets the scroll length for a mobile."""

    def tap_screen(self, element=None, config=None, x_cord=None, y_cord=None):
        """Perform tap for requested element or coordinates."""

    def swipe_up(self):
        """Swipe the screen to scroll down."""

    def swipe_right(self, config):
        """Swipe the screen to move right."""

    def press_long(self, hold_time, element=None, config=None, x_cord=None, y_cord=None):
        """Method to perform long press of element or a coordinate."""

    def press_long_and_slide(self, element, x_cord, y_cord, hold_time):
        """Method to perform long press of element or a coordinate."""

    def return_element(self, el_type, text, bounds=False):
        """Return element according to element type given."""

    def return_button(self, text, class_name='android.widget.TextView'):
        """Return element matching the text which is passed to it."""

    def click_element(self, el_type, text, delay, handle_error):
        """Search for element using accessibility id or xpath and click it."""

    def press_back(self, num=1):
        """Press back button on mobile for 'num' times."""

    def click_using_class(self, text, search_text, delay=3, is_button=False):
        """Return element according to 'text' or 'search text' and clicks it."""

    def start_app(self):
        """Open the application on the mobile device."""
