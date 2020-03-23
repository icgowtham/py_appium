"""WhatsApp class."""
import sys
import time

# Dependencies
from selenium.common.exceptions import NoSuchElementException

from apps.messaging.messaging import MessagingApp
# Import core modules
from core.logger import get_logger

LOGGER = get_logger().logger


class WhatsApp(MessagingApp):
    """Class containing methods for WhatsApp application."""

    def __init__(self, device_type):
        """Initialization Method."""
        app_name = 'WhatsApp'
        super().__init__(app_name, device_type)

    def upload_from_gallery(self, media_type, directory):
        """
        Select and send photo & video from different folders in gallery.

        :param media_type: str
            'Photo' or 'Video'
        :param directory: str
            Folder to find the media content (Example: Whatsapp Images, All Videos)
        :return: None
        """
        self.main_device.click_using_class(text=directory)
        self.main_device.click_element(el_type='xpath',
                                       text=self.config['XPATH_GALLERY'].format(media=media_type))
        time.sleep(3)
        self.main_device.click_element(el_type='access', text=self.config['SEND'])
        LOGGER.debug("{media} is sent!".format(media=media_type))

    def put_status(self, duration):
        """
        Triggers photo upload & clicking picture for status.
        Triggers video upload & capturing live video for status.

        :param duration: int
            Duration (in seconds) to record live video.
        :return: None
        """
        if duration > 30:
            LOGGER.info("Max. duration for live video 30 seconds."
                        "Set duration less than 30!", 'red')
            sys.exit(1)
        else:
            dur_milli_sec = duration * 1000  # Converting to milli-seconds
        LOGGER.info('Going to post photo & video as status!')
        self.main_device.click_using_class(text='STATUS')  # Open Status Menu
        # WhatsApp Status Update
        for media_type in self.config['MEDIA_LIST']:
            self.select_media_for_status(media_type)  # Selecting media using preview
            self.main_device.tap_screen(element='STATUS_BUTTON', config=self.config)
            self.live_media(media_type, vid_duration=dur_milli_sec)  # Live media capture for status

    def select_media_for_status(self, media_type):
        """
        Select one photo & video from preview & set it as status.

        :param media_type: str
            'Photo' or 'Video'
        :return: None
        """
        self.main_device.tap_screen(element='STATUS_BUTTON', config=self.config)
        time.sleep(2)
        i = 0
        while i == 0:
            try:
                # pylint: disable=line-too-long
                self.main_device.click_element(el_type='xpath',
                                               text=self.config['XPATH_GALLERY'].format(media=media_type),
                                               handle_error=False)
                time.sleep(3)
                break
            except NoSuchElementException:
                self.main_device.swipe_right(config=self.config)
        self.main_device.click_element(el_type='access', text=self.config['SEND'])
        LOGGER.debug("{media} status is set on {name}!".format(
            media=media_type, name=self.main_device.mobile_name))

    def live_media(self, media_type, vid_duration):
        """
        Capture one photo and one live video & set it as status.

        :param media_type: str
            'Photo' or 'Video'
        :param vid_duration: int
            Duration (in seconds) to record live video
        :return: None
        """
        LOGGER.info("Preparing to capture {media}...".format(media=media_type))
        time.sleep(2)
        if media_type == 'Photo':
            self.main_device.tap_screen(element='LIVE_RECORD', config=self.config)
        else:
            self.main_device.press_long(x_cord=self.config['LIVE_RECORD']['x'],
                                        y_cord=self.config['LIVE_RECORD']['y'],
                                        hold_time=vid_duration)
            time.sleep(10)

        self.main_device.click_element(el_type='access', text=self.config['SEND'])
        LOGGER.debug("Captured {media} sent!".format(media=media_type))

    def send_media_from_gallery(self):
        """
        Attach photo & video from gallery and send to contact.

        :return: None
        """
        for media_type in self.config['MEDIA_LIST']:
            self.main_device.click_element(el_type='access', text='Attach')
            LOGGER.info("Preparing to send {media} from {name}".format(
                media=media_type, name=self.main_device.mobile_name))
            self.main_device.click_using_class(text='Gallery')
            self.upload_from_gallery(media_type, self.config['FOLDER_DICT'][media_type])

    def send_instant_media(self, duration):
        """
        Record audio, click photo & capture live video using Camera button for sending to contact.

        :param duration: int
            Duration (in seconds) to capture the live video & record audio
        :return: None
        """
        # Record audio
        dur_milli_sec = duration * 1000  # Converting to milli-seconds
        LOGGER.info("Starting to record audio...")
        time.sleep(2)
        voice_record = self.main_device.return_element(el_type='access',
                                                       text='Voice note recorder')
        self.main_device.press_long(element=voice_record, hold_time=dur_milli_sec)
        LOGGER.debug('Sent recorded audio!')
        # Photo & video
        for media in self.config['MEDIA_LIST']:
            camera = self.main_device.return_element(el_type='access',
                                                     text='Camera')
            camera.click()
            self.live_media(media, vid_duration=dur_milli_sec)

    def share_files(self):
        """
        Attach a document & send to contact.

        :return: None
        """
        self.main_device.click_element(el_type='access', text='Attach')
        LOGGER.info("Preparing to send document from {name}".format(
            name=self.main_device.mobile_name))
        self.main_device.click_using_class(text='Document')
        i = 0
        while i == 0:
            try:
                self.main_device.click_using_class(text=self.config['DOC_FILE'])
                self.main_device.click_element(el_type='access', text=self.config['SEND'])
                LOGGER.debug("Document sent!")
                i = 1
            except NoSuchElementException:
                self.main_device.swipe_up()
                time.sleep(2)

    @staticmethod
    def click_contact(dev_1, dev_2):
        """
        Click a contact and open chat.

        :return: None
        """
        for dev in (dev_1, dev_2):
            dev.click_using_class(text='CHATS', delay=5)  # Return to Chats Menu
            dev.click_using_class(dev.contact)  # Open contact on mobile

    def perform_one_side_calls(self, duration):
        """
        Give audio call & video call from secondary mobile. Main mobile will not attend the call.

        :param duration: int
            Duration (in seconds) to hold the call ringing
        :return: None
        """
        for call_type in self.config['CALL_LIST']:
            self.give_call(call_type, duration)

    def give_call(self, call_type, duration):
        """
        Initiate audio / video call & cut the call after specified duration.

        :param dev: device object
            Device on which this action has to be performed
        :param call_type: str
            'audio' or 'video'
        :param duration: int
            Duration (in seconds) to hold before cutting the call
        :return: None
        """
        self.initiate_call(call_type)
        time.sleep(duration)
        self.second_device.tap_screen(element='END_CALL', config=self.config)  # End call button
        LOGGER.info("Closed {media} call!".format(media=call_type))
        time.sleep(4)

    def initiate_call(self, call_type):
        """
        Initiates the call from second mobile.

        :param dev: device object
            Device on which this action has to be performed.
        :param call_type: str
            'audio' or 'video'
        :return: None
        """
        time.sleep(5)
        LOGGER.info("Initiating WhatsApp {media} call now...".format(media=call_type))
        self.second_device.click_element(el_type='access', text=self.config['CALL_DICT'][call_type])

    def accept_call(self, call_type, duration):
        """
        Accept incoming audio / video call from second mobile.

        :param call_type: str
            'audio' or 'video'
        :param duration: int
            Duration (in seconds) to keep the call alive
        :return: None
        """
        while True:
            try:
                green_button = self.main_device.return_element(el_type='access',
                                                               text=self.config['ACCEPT_CALL'])
                self.main_device.press_long_and_slide(element=green_button,
                                                      x_cord=self.config['END_CALL']['x'],
                                                      y_cord=(self.config['END_CALL']['y'] - 300),
                                                      hold_time=500)
                time.sleep(duration)
                LOGGER.info("Attended WhatsApp {media} call!".format(media=call_type))
                self.main_device.tap_screen(element='END_CALL', config=self.config)
                break
            except NoSuchElementException:
                LOGGER.info('Ringing...')

    def perform_chat(self):
        """
        Peform Whatsapp chat using two devices.

        :return: None
        """
        LOGGER.info("Starting chat now..")
        time.sleep(3)
        for mobile in (self.main_device, self.second_device):
            for word in self.config['CHAT_LIST']:
                mobile.click_using_class(search_text='Type a message', text=word, delay=1)
                mobile.click_element(el_type='access', text=self.config['SEND'], delay=1)
        # Send emoji
        self.main_device.click_element(el_type='access', text='Emoji')
        LOGGER.info('Sending emoji...')
        local_dict = self.config['EMOJI']
        for row in (local_dict['y'], local_dict['y'] + 115):
            for emoji in range(local_dict['x'], local_dict['x'] + 600, 120):
                self.main_device.tap_screen(x_cord=emoji, y_cord=row)
                LOGGER.info("pressed emoji button!")
                time.sleep(2)
            self.main_device.click_element(el_type='access', text=self.config['SEND'], delay=1)
        self.main_device.press_back(2)
        LOGGER.debug("Chat Finished!")

    def make_call_two_mobiles(self, duration=15):
        """
        Second device will call & Main device will attend call for specified duration.

        :param duration: int
            Duration (in seconds) for the calls. Defaults to 15 seconds.
        :return: None
        """
        self.main_device.press_back(4)
        for call_type in self.config['CALL_LIST']:
            self.initiate_call(call_type)
            self.accept_call(call_type, duration)
            if call_type == 'video':
                self.main_device.tap_screen(element='END_CALL', config=self.config)
            LOGGER.debug('{cal} call ended!'.format(cal=call_type))

    def all_features(self):
        """Run all automation features of WhatsApp."""
        LOGGER.info('Starting WhatsApp automation now..!')
        self.put_status(duration=10)
        WhatsApp.click_contact(self.main_device, self.second_device)
        self.send_media_from_gallery()
        self.share_files()
        self.send_instant_media(duration=10)
        self.perform_one_side_calls(duration=7)
        self.perform_chat()
        self.make_call_two_mobiles(duration=15)
