"""Facebook class."""
import time
from random import randint

from selenium.common.exceptions import NoSuchElementException

from apps.social.social import SocialApp
# Import core modules
from core.logger import get_logger

LOGGER = get_logger().logger


class Facebook(SocialApp):
    """Class containing methods for Facebook application."""

    RAND_NUM = randint(0, 4)

    def __init__(self, device_type):
        """Initialization Method."""
        app_name = 'Facebook'
        super().__init__(app_name, device_type)

    def watch_videos(self, duration):
        """
        Watch videos for specified duration.

        :param duration: int
            Duration (in seconds) to watch facebook videos
        :return: None
        """
        LOGGER.info("Going to watch videos now...")
        self.main_device.tap_screen('MENU', config=self.config)  # Menu button
        time.sleep(3)
        self.main_device.click_element(el_type='access', text='Videos on Watch', delay=duration)
        LOGGER.debug("Finished watching videos for {dur} seconds!".format(dur=duration))
        self.main_device.press_back()

    def go_live(self, duration):
        """
        Capture video and go live on Facebook.

        :param duration: int
            Duration (in seconds) to capture the live video
        :return: None
        """
        self.main_device.click_element(el_type='xpath', text=self.config['LIVE_VIDEO'])
        LOGGER.info("Going to start live video...")
        self.main_device.click_using_class(text='Start Live Video',
                                           delay=duration)  # Start live video
        self.main_device.click_using_class(text='FINISH', delay=(duration + 10),
                                           is_button=True)  # Finish button
        LOGGER.info("Live video finished.")
        self.main_device.click_using_class(text='SHARE', delay=5, is_button=True)  # Share button
        LOGGER.debug("Live video was shared!")

    def instant_media_upload(self, duration):
        """
        Capture live video, click picture and post on Facebook.

        :param duration: int
            Duration (in seconds) to capture the live video
        :return: None
        """
        for media in ('Photo', 'Video'):
            LOGGER.info("Going to capture {med}...".format(med=media))
            self.main_device.click_element(el_type='xpath', text=self.config['PHOTO_UPLOAD'],
                                           delay=7)
            self.main_device.click_element(el_type='access', text='Camera')
            if media == 'Photo':
                self.main_device.tap_screen(element='CAM', config=self.config)
            else:
                self.main_device.click_using_class(text='VIDEO', is_button=True)
                self.main_device.tap_screen(element='CAM', config=self.config)  # Start video
                time.sleep(duration)
                self.main_device.tap_screen(element='CAM', config=self.config)  # end video
                time.sleep(2)
            self.main_device.click_using_class(text='DONE', delay=5)
            self.main_device.click_element(el_type='access', text=self.config['POST'])
            LOGGER.debug("{med} Uploaded successfully!".format(med=media))

    def check_in(self):
        """
        Perform check-in of a location on Facebook.

        :return: None
        """
        LOGGER.info("Going to Check-in now...")
        self.main_device.click_element(el_type='xpath', text=self.config['CHECK_IN'])
        self.main_device.click_using_class(search_text='Search for places',
                                           text=self.config['LOC_TUPLE'][Facebook.RAND_NUM])
        self.main_device.press_using_keycode('search')  # Press Search button
        self.main_device.tap_screen('RANDOM', config=self.config)  # To select a check-in place
        try:
            self.main_device.click_element(el_type='access', text='SKIP')
            self.main_device.click_element(el_type='access', text=self.config['POST'], delay=5)
        except NoSuchElementException:
            self.main_device.click_element(el_type='access', text=self.config['POST'], delay=5)
        LOGGER.debug("Check-in was posted successfully!")
        self.main_device.tap_screen('RANDOM',
                                    config=self.config)  # Skip question about check-in

    def gallery_media_upload(self):
        """
        Upload photo and video from gallery on Facebook.

        :return: None
        """
        for media in ('Photo', 'Video'):
            LOGGER.info("Going to upload {med}...".format(med=media))
            self.main_device.click_element(el_type='xpath', text=self.config['PHOTO_UPLOAD'],
                                           delay=7)
            self.main_device.click_element(el_type='xpath',
                                           text=self.config['UPLOAD_MEDIA'].format(med=media),
                                           delay=7)
            self.main_device.click_element(el_type='access', text='NEXT', delay=7)
            self.main_device.click_element(el_type='access', text=self.config['POST'])
            LOGGER.debug("{med} Uploaded successfully!".format(med=media))

    def like_comment_share(self):
        """
        Perform like, share & comment on posts on Facebook.

        :return: None
        """
        for _11 in range(0, 5):  # _11 as dummy variable
            try:
                self.main_device.click_using_class(text='Like')
                LOGGER.debug("Liked a post!")
                self.main_device.click_using_class(text='Comment')
                self.main_device.click_using_class(search_text='Write a comment…',
                                                   text=self.config['WORD_COMMENT'])
                self.main_device.click_element(el_type='access', text='Send',
                                               delay=5, handle_error=False)
                LOGGER.debug("Commented on a post!")
                self.main_device.press_back(2)
                time.sleep(3)
                self.main_device.click_element(el_type='xpath', text=self.config['SHARE_POST'],
                                               handle_error=False)
                self.main_device.click_element(el_type='access', text='SHARE NOW',
                                               handle_error=False)
                LOGGER.debug("Shared a post!")
                break
            except NoSuchElementException:
                self.main_device.swipe_up()
        self.main_device.press_back()

    def send_friend_request(self):
        """
        Send a friend request. If request exists, cancel friend request.

        :return: None
        """
        self.main_device.tap_screen('HOME', config=self.config)  # Tap Home button
        self.main_device.tap_screen('SEARCH', config=self.config)  # Tap Search button
        self.main_device.click_using_class(search_text='Search',
                                           text=self.config['FRIEND'])
        self.main_device.press_using_keycode('enter')  # Press Enter
        try:
            self.main_device.click_element(el_type='xpath', text=self.config['ADD_FRIEND'],
                                           handle_error=False)
            LOGGER.debug("Sent friend request!")
        except NoSuchElementException:
            self.main_device.click_element(el_type='access', text='Cancel friend request')
            LOGGER.debug("Cancelling friend request now!")
        self.main_device.press_back(3)

    def all_features(self):
        """Run all automation features of Facebook."""
        LOGGER.info("Starting Facebook automation now..!")
        self.send_friend_request()
        self.gallery_media_upload()
        self.go_live(duration=10)
        self.instant_media_upload(duration=10)
        self.check_in()
        self.watch_videos(duration=20)
        self.like_comment_share()
        self.send_friend_request()
