"""YouTube class."""
import time
from random import randint

# Dependencies
from selenium.common.exceptions import NoSuchElementException

from apps.streaming.streaming import StreamingApp
# Import Core modules
from core.logger import get_logger

LOGGER = get_logger().logger


class YouTube(StreamingApp):
    """Class containing methods for YouTube application."""

    RAND_NUM = randint(0, 4)

    def __init__(self, device_type):
        """Initialization Method."""
        app_name = 'YouTube'
        super().__init__(app_name, device_type)
        self.main_device.contact = self.config['CONTACT'][self.main_device.mobile_name]

    def upload_video(self, duration):
        """
        Upload video on Youtube by recording live video.

        :param duration: int
            Duration (in seconds) to record video on Youtube
        :return: None
        """
        LOGGER.info("Going to record video for upload...")
        self.main_device.click_element(el_type='access', text='Video')
        self.main_device.click_using_class(text='RECORD')  # Open Camera
        try:
            record_circle = self.main_device.return_element(el_type='id',
                                                            text=self.config['RECORD_CIRCLE'])
            record_circle.click()  # Start Record
            time.sleep(duration)
            record_circle.click()  # Stop Record
            time.sleep(duration + 10)
        except NoSuchElementException:
            self.main_device.tap_screen(x_cord=276, y_cord=1771)
            time.sleep(duration)
            self.main_device.return_button(text='Stop', class_name='GLButton').click()
            time.sleep(3)
            self.main_device.click_using_class(text='OK')
        self.main_device.click_using_class(text='UPLOAD', delay=10)
        LOGGER.debug("Uploaded video!")
        self.main_device.press_back()

    def click_tabs_and_scroll_through(self):
        """
        Click different tabs present in Youtube and scroll through them.

        :return: None
        """
        for button in self.config['BUTTONS']:
            self.main_device.tap_screen(button, config=self.config)
            LOGGER.debug("Pressed {but} button. Scrolling now..".format(but=button))
            time.sleep(2)
            for __11 in range(0, 4):  # _11 as dummy variable
                self.main_device.swipe_up()
                time.sleep(1)
        # Return to home screen
        self.main_device.tap_screen('HOME', config=self.config)

    def click_next_video(self):
        """
        Method to click the next video.

        :return: None
        """
        bounds_list = self.main_device.return_element(el_type='xpath',
                                                      text=self.config['CLICK_VIDEO'],
                                                      bounds=True)
        x_cor = bounds_list[1:5]
        y_cor = bounds_list[(-5):(-1)]

        if x_cor.endswith(','):
            x_cor = int(bounds_list[1:4]) - 200
        else:
            x_cor = int(x_cor) - 200

        if y_cor.startswith(','):
            y_cor = int(bounds_list[(-4):(-1)]) - 100
        else:
            y_cor = int(y_cor) - 100

        self.main_device.tap_screen(x_cord=x_cor, y_cord=y_cor)

    def watch_videos(self, num_vid, duration=10):
        """
        Search and watch videos on Youtube.

        :param num_vid: int
            Number of videos to watch
        :param duration: int
            Duration (in seconds) to watch each video. Defaults to 10 seconds.
        :return: None
        """
        LOGGER.info("Going to search videos...")
        self.main_device.click_element(el_type='access', text='Search')
        self.main_device.click_using_class(search_text='Search YouTube',
                                           text=self.config['SEARCH_TUPLE'][YouTube.RAND_NUM])
        self.main_device.press_using_keycode('enter')  # Enter button
        vid_count = 0
        while vid_count < num_vid:
            try:
                self.click_next_video()
                vid_count += 1
                LOGGER.debug("Playing video {num}!".format(num=vid_count))
                time.sleep(duration)
            except NoSuchElementException:
                self.main_device.swipe_up()
            # To skip app advertisement and live chat
            element = self.main_device.return_button('Live chat')
            if element:
                self.main_device.click_element(el_type='access', text='Close')
            else:
                try:
                    ad_panel = self.main_device.return_element(el_type='access',
                                                               text='Close ad panel')
                    ad_panel.click()
                except NoSuchElementException:
                    continue

    def share_download_save(self):
        """
        Share Youtube video link on Whatsapp. Download and save videos.

        :return: None
        """
        count_share = 0
        count_save = 0
        count_download = 0
        duration = 10
        # Share, Download and Save to Watchlist
        elements = self.main_device.return_textview_elements()
        for button in elements:
            if count_share > 0 and count_save > 0 and count_download > 0:
                break

            if count_share == 0 and button.text == 'Share':
                LOGGER.info("Going to share video...")
                button.click()
                time.sleep(duration - 3)
                try:
                    self.main_device.click_using_class(text='WhatsApp')
                except NoSuchElementException:
                    self.main_device.swipe_up()
                    self.main_device.click_using_class(text='WhatsApp')
                self.main_device.click_using_class(text=self.main_device.contact)
                self.main_device.click_element(el_type='access', text='Send')
                time.sleep(2)
                self.main_device.click_element(el_type='access', text='Send')
                LOGGER.debug('Shared video link!')
                self.main_device.press_back(2)
                count_share += 1

            if count_save == 0 and button.text == 'Save':
                LOGGER.info("Going to save video...")
                button.click()
                LOGGER.debug('Saved video!')
                time.sleep(duration + 5)
                count_save += 1

            if count_download == 0 and button.text == 'Download':
                LOGGER.info("Going to download video...")
                button.click()
                LOGGER.debug('Downloaded video!')
                time.sleep(duration + duration)
                count_download += 1

            if count_download == 0 and button.text == 'Downloaded':
                LOGGER.info('This video has already been downloaded! '
                            'Will download another video now')
                self.main_device.swipe_up()
                time.sleep(2)
                self.main_device.click_element(el_type='xpath', text=self.config['CLICK_VIDEO'])
                LOGGER.info("Going to download video...")
                self.main_device.click_using_class(text='Download')
                count_download += 1
                LOGGER.debug('Downloaded video!')

        self.main_device.press_back(2)

    def all_features(self):
        """Run all automation features of Youtube."""
        LOGGER.info("Starting YouTube automation now..!")
        self.upload_video(duration=2)
        self.click_tabs_and_scroll_through()
        self.watch_videos(num_vid=2, duration=20)
        self.share_download_save()
