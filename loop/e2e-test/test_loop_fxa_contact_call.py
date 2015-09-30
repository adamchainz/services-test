from marionette_driver.by import By
from marionette_driver.errors import NoSuchElementException, StaleElementException
# noinspection PyUnresolvedReferences
from marionette_driver import Wait
from marionette import MarionetteTestCase

import os
import sys
import urlparse
import pyperclip
import time
from six.moves import input
sys.path.insert(1, os.path.dirname(os.path.abspath(__file__)))
from config import *

MASTER_EMAIL = 'tryloopprod@mailinator.com'
MASTER_PASSWORD = 'tryloopprod'
HELPER_NAME = 'Johnny Quest'
HELPER_EMAIL = 'tryloopprod2@mailinator.com'
HELPER_PASSWORD = 'tryloopprod2'


class TestLoopFxaContactCall(MarionetteTestCase):

    def setUp(self):
        MarionetteTestCase.setUp(self)
        self.marionette.enforce_gecko_prefs(FIREFOX_PREFERENCES)
        self.marionette.set_context(self.marionette.CONTEXT_CHROME)

    def debug_show_content(self, context):
        self.marionette.set_context(context)
        print(self.marionette.page_source)

    def switch_to_panel(self):
        self.marionette.set_context(self.marionette.CONTEXT_CHROME)
        self.marionette.switch_to_frame()
        hello_button = self.marionette.find_element(By.ID, "loop-button")
        hello_button.click()

        frame = self.marionette.find_element(By.ID, "loop-panel-iframe")
        self.marionette.switch_to_frame(frame)

    def switch_to_chatbox(self):
        self.marionette.set_context(self.marionette.CONTEXT_CHROME)
        self.marionette.switch_to_frame()

        chatbox = self.wait_for_element_exists(By.TAG_NAME, 'chatbox')
        script = ("return document.getAnonymousElementByAttribute("
                                "arguments[0], 'class', 'chat-frame');")
        frame = self.marionette.execute_script(script, [chatbox])
        self.marionette.switch_to_frame(frame)

    def wait_for_element_displayed(self, by, locator, timeout=None):
        Wait(self.marionette, timeout, ignored_exceptions=[NoSuchElementException, StaleElementException])\
                .until(lambda m: m.find_element(by, locator).is_displayed())
        return self.marionette.find_element(by, locator)

    def wait_for_element_exists(self, by, locator, timeout=None):
        Wait(self.marionette, timeout, ignored_exceptions=[NoSuchElementException, StaleElementException]) \
            .until(lambda m: m.find_element(by, locator))
	return self.marionette.find_element(by, locator)

    def wait_for_element_enabled(self, element, timeout=10):
        Wait(self.marionette, timeout) \
            .until(lambda e: element.is_enabled(), message="Timed out waiting for element to be enabled")

    def local_fxa_sign_in(self):
        button = self.marionette.find_element(By.CLASS_NAME, "sign-in-request-button")
        self.wait_for_element_enabled(button, 120)
        button.click()

    def local_go_to_link(self, url):
        # we need to set_context to 'content' to navigate
        self.marionette.set_context(self.marionette.CONTEXT_CONTENT)
        self.marionette.navigate(url)

    def local_fxa_enter_password(self):
        self.marionette.set_context(self.marionette.CONTEXT_CONTENT)
        self.marionette.switch_to_frame()
        original_window = self.marionette.current_window_handle
        for handle in self.marionette.window_handles:
            print 'handle: {0}'.format(handle)
        #    if handle != original_window:
        #        print 'switching to handle: {0}'.format(handle)
        #        self.marionette.switch_to_window(handle)
                

        # this is a hack - we're assuming window_handles is either
        # original or NOT.  we don't want the original, so we want
        # the other one - FxA login window.
        self.marionette.switch_to_window(handle)
        # why do we need this?
        time.sleep(3)

        input_box = self.marionette.find_element(By.ID, "password")
        self.wait_for_element_enabled(input_box, 120)
        input_box.send_keys(MASTER_PASSWORD)
        time.sleep(3)
        
        button = self.marionette.find_element(By.ID, "submit-btn")
        self.wait_for_element_enabled(button, 120)
        button.click()

    def local_fxa_contacts_tab(self):

        button = self.marionette.find_element(By.XPATH, './/*[@data-tab-name="contacts"]')
        self.wait_for_element_enabled(button, 120)
        button.click()
        time.sleep(5)

    def local_fxa_contacts_add(self):

        button = self.marionette.find_element(
            By.XPATH, "//*[text() = 'Add new contact' or text() = 'New Contact']"
        )
        self.wait_for_element_enabled(button, 120)
        button.click()
        time.sleep(5)
        #button = self.marionette.find_element(By.XPATH, './/*[@placeholder="Name"]')
        button = self.marionette.find_element(By.XPATH, './/input[@type="text"]')
        self.wait_for_element_enabled(button, 120)
        button.send_keys(HELPER_NAME)
        time.sleep(5)
        #button = self.marionette.find_element(By.XPATH, './/*[@placeholder="Email"]')
        button = self.marionette.find_element(By.XPATH, './/input[@type="email"]')
        self.wait_for_element_enabled(button, 120)
        #button.send_keys("peter@deseloper.com")
        button.send_keys(HELPER_EMAIL)
        time.sleep(5)
        button = self.marionette.find_element(By.CLASS_NAME, "button-accept") 
        self.wait_for_element_enabled(button, 120)
        button.click()
        time.sleep(5)

    def local_fxa_start_a_conversation(self):
        # you must first have a contact in your contacts!
        # OSX:    icon-contact-video-call
        # LINUX:  icon-video-call

        #link = self.marionette.find_element(By.CLASS_NAME, "icon-contact-video-call")
        link = self.marionette.find_element(
            By.XPATH, 
            "//i[contains(@class, 'icon-contact-video-call') or contains(@class, 'icon-video-call')]"
        )
        self.wait_for_element_enabled(link, 120)
        link.click()

    def local_start_a_conversation(self):
        button = self.marionette.find_element(By.CSS_SELECTOR, ".rooms .btn-info")
        self.wait_for_element_enabled(button, 120)
        button.click()

    def local_get_and_verify_room_url(self):
        self.switch_to_chatbox()
        # should wait for char box to show instead of sleeping once
        time.sleep(3)
        button = self.wait_for_element_displayed(By.CLASS_NAME, "btn-copy")
        self.wait_for_element_enabled(button)
        button.click()
        room_url = pyperclip.paste()
        self.assertIn(
            urlparse.urlparse(room_url).scheme, 
            ['http', 'https'],
            "room URL returned by server: '" + room_url +
            "' has invalid scheme"
        )
        return room_url

    def local_get_chatbox_window_expr(self, expr):
        """
        :expr: a sub-expression which must begin with a property of the
        global content window (e.g. "location.path")

        :return: the value of the given sub-expression as evaluated in the
        chatbox content window
        """
        self.marionette.set_context(self.marionette.CONTEXT_CHROME)
        self.marionette.switch_to_frame()

        # XXX should be using wait_for_element_displayed, but need to wait
        # for Marionette bug 1094246 to be fixed.
        chatbox = self.wait_for_element_exists(By.TAG_NAME, 'chatbox')
        script = '''
            let chatBrowser = document.getAnonymousElementByAttribute(
              arguments[0], 'class',
              'chat-frame')

            // note that using wrappedJSObject waives X-ray vision, which
            // has security implications, but because we trust the code
            // running in the chatbox, it should be reasonably safe
            let chatGlobal = chatBrowser.contentWindow.wrappedJSObject;

            return chatGlobal.''' + expr

        return self.marionette.execute_script(script, [chatbox])


    def local_get_media_start_time(self):
        return self.local_get_chatbox_window_expr(
            "loop.conversation._sdkDriver._getTwoWayMediaStartTime()"
        )

    def local_get_media_start_time_uninitialized(self):
	return self.local_get_chatbox_window_expr(
            "loop.conversation._sdkDriver.CONNECTION_START_TIME_UNINITIALIZED"
        )

    def local_check_media_start_time_uninitialized(self):
        print(self.local_get_media_start_time())
        print(self.local_get_media_start_time_uninitialized())
        self.assertEqual(
            self.local_get_media_start_time(),
            self.local_get_media_start_time_uninitialized(),
            "media start time should not be initialized before link clicker enters room"
        )

    def test_loop_fxa_contact_call(self):

        # CHATBOX
        self.switch_to_panel()
        time.sleep(3)
        self.local_fxa_sign_in()
        time.sleep(3)

        # BROWSER
        self.local_fxa_enter_password()
        time.sleep(6)

        # CHATBOX
        self.switch_to_panel()
        time.sleep(6)
        self.local_fxa_contacts_tab()
        time.sleep(6)
        self.local_fxa_contacts_add()
        time.sleep(6)
        self.local_fxa_start_a_conversation()
        time.sleep(180)

    def tearDown(self):
        MarionetteTestCase.tearDown(self)
