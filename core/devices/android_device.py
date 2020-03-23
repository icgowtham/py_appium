"""Android Device class for performing actions on android app."""
import os
import subprocess
import sys
import time

# Import Dependencies
from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
from selenium.common.exceptions import WebDriverException, NoSuchElementException

# Import core modules
from core.devices.device import Device
from core.logger import get_logger

LOGGER = get_logger().logger

KEY_CODE_DICT = {
    'enter': 66,
    'search': 84
}


# pylint: disable=too-many-instance-attributes
class AndroidDevice(Device):
    """Android driver class."""

    def __init__(self, app_name, app_server):
        """Initialization Method."""
        super().__init__(app_name)
        self.driver = None
        self.touch = None
        self.mobile_name = None
        self.contact = None
        self.create_driver(app_server)

    def create_driver(self, app_server):
        """
        Create a driver to the specified appium server & return driver,touch objects.

        :param app_server: str
            'SERVER_1' or 'SERVER_2'
        :return: driver object, touch object, mobile name
            Return driver, touch objects & mobile name for specified appium server.
        """
        config = self.config[app_server]

        cmd = config['CMD']
        server_name = config['NAME']
        log_file_name = config['LOG_FILE_NAME']
        full_log_path = os.path.join(os.environ['basedir'], 'logs', 'appium', log_file_name)
        url = config['URL']
        desired_cap = config['DESIRED_CAP']
        self.mobile_name = config['MOBILE_NAME']

        with open(full_log_path, "w") as file:
            subprocess.Popen(cmd, shell=True, stdout=file, stderr=subprocess.STDOUT)
        LOGGER.info("{name} started !".format(name=server_name))
        try:
            self.driver = webdriver.Remote(url, desired_cap)
            self.touch = TouchAction(self.driver)
            LOGGER.info("Connected to {mob}".format(mob=self.mobile_name))
        except WebDriverException:
            LOGGER.error("{dev} is not connected!".format(
                dev=self.mobile_name))
        time.sleep(3)

    def close_driver(self):
        """
        Close the application, quits the drivers.

        :return: None
        """
        package_dict = self.config['PACKAGE']
        try:
            self.driver.terminate_app(package_dict[self.app_name])  # Kill app
            self.driver.quit()  # Kill drivers
        except WebDriverException:
            pass
        finally:
            LOGGER.info("Closed {apl} on {mob}!".format(
                apl=self.app_name, mob=self.mobile_name))

    def set_scroll_length(self):
        """
        Read mobile window size & sets the scroll length for a mobile.

        :return: None
        """
        size = self.driver.get_window_size()
        self.x_cord = int(size['width'] / 2)
        self.start_y = int(size['height'] * 0.9)
        self.end_y = int(size['height'] * 0.1)

    # pylint: disable=C0103
    def tap_screen(self, element=None, config=None, x_cord=None, y_cord=None):
        """
        Perform tap for requested element or coordinates.

        :param config: dict
            Config dictionary of particular app
        :param element: str
            Where tap has to be performed. (Example: 'Home' , 'Search')
        :param x_cord:  int
            X coordinate of element to tap.
        :param y_cord: int
            Y coordinate of element to tap.
        :return: None
        """
        if element and config:
            self.touch.tap(x=config[element]['x'],
                           y=config[element]['y']).perform()
        elif x_cord:
            self.touch.tap(x=x_cord, y=y_cord).perform()
        else:
            LOGGER.error('Either element or co-ordinates must be given for tap!')
        time.sleep(2)

    def swipe_up(self):
        """
        Swipe the screen to scroll down.

        :return: None
        """
        self.driver.swipe(start_x=self.x_cord, start_y=self.start_y,
                          end_x=self.x_cord, end_y=self.end_y, duration=1000)

    def swipe_right(self, config):
        """
        Swipe the screen to move right.

        :return: None
        """
        self.driver.swipe(start_x=config['SWIPE_RIGHT']['x'],
                          start_y=config['SWIPE_RIGHT']['y'],
                          end_x=(config['SWIPE_RIGHT']['x'] - 400),
                          end_y=config['SWIPE_RIGHT']['y'], duration=1000)

    # pylint: disable=too-many-arguments
    def press_long(self, hold_time, element=None, config=None, x_cord=None, y_cord=None):
        """
        Method to perform long press of element or a coordinate.

        :param config: dict
            Config file for particular application.
        :param hold_time: int
            Duration (in milli-seconds) for which long press must be performed
        :param element: obj
            Element on which long press has to be performed.
        :param x_cord: int
            X coordinate of element
        :param y_cord: int
            Y coordinate of element
        :return: None
        """
        if config:
            self.touch.long_press(x=config[element]['x'],
                                  y=config[element]['y'],
                                  duration=hold_time).release().perform()
        elif element:
            self.touch.long_press(el=element, duration=hold_time).release().perform()
        elif x_cord:
            self.touch.long_press(x=x_cord, y=y_cord, duration=hold_time).release().perform()
        else:
            LOGGER.error('Either element or co-ordinates must be given for long press!')
        time.sleep(2)

    def press_long_and_slide(self, element, x_cord, y_cord, hold_time):
        """
        Method to perform long press of element or a coordinate and slide.

        :param element: obj
            Element on which long press has to be performed.
        :param x_cord: int
            X coordinate of element
        :param y_cord: int
            Y coordinate of element
        :param hold_time: int
            Duration (in milli-seconds) for which long press must be performed
        :return: None
        """
        if element:
            self.touch.long_press(el=element, duration=hold_time).move_to(
                x=x_cord, y=y_cord).release().perform()
        else:
            LOGGER.error('Element and co-ordinates must be given for long press!')

    def press_using_keycode(self, text):
        """
        Select an key on the screen using keycode.

        :param text: str
            Text for which key code number has to be found. Example: 'enter', 'search'.
        :return: None
        """
        num = KEY_CODE_DICT[text]
        self.driver.press_keycode(num)
        time.sleep(3)

    def press_back(self, num=1):
        """
        Press back button on mobile for 'num' times.

        :param num: int
            Number of times to press back button. Defaults to 1.
        :return: None
        """
        for _11 in range(0, num):  # _11 as dummy variable
            self.driver.back()

    def return_element(self, el_type, text, bounds=False):
        """
        Return element according to element type given.

        :param el_type: str
            type of element: 'access', 'id', 'xpath'
        :param text: str
            String by which element is identified.
        :param bounds: Boolean
            If 'True', bounds of the element will be returned.
        :return: element
            Returns respective element based on element type.
        """
        if el_type == 'access':
            element = self.driver.find_element_by_accessibility_id(text)
        elif el_type == 'id':
            element = self.driver.find_element_by_id(text)
        elif el_type == 'xpath' and bounds:
            element = self.driver.find_element_by_xpath(text).get_attribute('bounds')
        elif el_type == 'xpath':
            element = self.driver.find_element_by_xpath(text)
        else:
            element = None
            LOGGER.error('No match found for input parameters!')
        return element

    def return_textview_elements(self):
        """
        Return list of elements of class 'android.widget.TextView'.

        :return: list of elements
            Returns list of elements for class 'android.widget.TextView'
        """
        return self.driver.find_elements_by_class_name('android.widget.TextView')

    def return_button(self, text, class_name='android.widget.TextView'):
        """
        Return element matching the text which is passed to it.

        :param text: str
            Text present in the element.
        :param class_name: str
            Class to which the element belongs to. Defaults to 'android.widget.TextView'.
        :return: object
            Returns element if present. Returns 'None' if element not found.
        """
        for button in self.driver.find_elements_by_class_name(class_name):
            if button.text == text:
                return button
        return None

    def click_element(self, el_type, text, delay=3, handle_error=True):
        """
        Click a specified element if present. Handles error inside the method if parameter is set.

        :param el_type: str
            'access' or 'xpath' accordingly to the element present.
        :param text: str
            accessibility id or xpath string to identify the element.
        :param delay: int
            Delay in seconds after clicking the text. Defaults to 3 seconds.
        :param handle_error: Boolean
            If set to 'True', handles exception inside the method.
        :return: None
        """
        if el_type not in ['access', 'xpath']:
            LOGGER.error('Mentioned element does not exist!')
            button = None
        else:
            button = self.return_element(el_type=el_type, text=text)

        if handle_error:
            try:
                button.click()
            except NoSuchElementException:
                LOGGER.error('{ele} is not found: {err}'.format(ele=el_type, err=text))
                sys.exit(1)
        else:
            button.click()
        time.sleep(delay)

    def click_using_class(self, text, search_text=None, delay=3, is_button=False):
        """
        Return element according to 'text' or 'search text' and clicks it.

        :param text: str
            Text to click on the screen.
            In case of search box, text to enter into box  (Eg:'Phoenix Mall')
        :param search_text: str
            Name of the search box to click (Example: 'Type a message')
        :param delay: int
            Delay in seconds after clicking the text. Defaults to 3 seconds.
        :param is_button: Boolean
            Whether element is button or not. Defaults to 'False'.
        :return: None
        :raises: NoSuchElementException
            Raises NoSuchElementException if element not found.
        """
        if search_text:
            class_name = 'android.widget.EditText'
            button = self.return_button(search_text, class_name)
        elif is_button:
            class_name = 'android.widget.Button'
            button = self.return_button(text, class_name)
        else:
            class_name = 'android.widget.TextView'
            button = self.return_button(text, class_name)

        if not button:
            raise NoSuchElementException

        if search_text:
            button.send_keys(text)
        else:
            button.click()
        time.sleep(delay)

    def start_app(self):
        """
        Open application on mobile device.

        :return: None
        """
        app_xpath = '//android.widget.FrameLayout[@content-desc=\"{app}\"]/android.widget.ImageView'
        LOGGER.info('Starting app now!')
        tex = app_xpath.format(app=self.app_name)
        try:
            self.click_element(el_type='xpath', text=tex, handle_error=False)
        except NoSuchElementException:
            LOGGER.exception('Cannot find {app} on home screen of the phone!'.format(
                app=self.app_name))
            sys.exit(1)
        LOGGER.debug("{app} is opened on {name}".format(
            app=self.app_name, name=self.mobile_name))
        time.sleep(5)
        self.set_scroll_length()
