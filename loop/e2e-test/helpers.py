from marionette_driver.errors import NoSuchElementException, StaleElementException
from marionette_driver import By, Wait
import pyperclip
import pytest
import time


@pytest.mark.usefixtures('conf', 'env', 'marionette', 'puppeteer')
class Helpers():
    def setUp(self, conf, env, marionette, puppeteer):
        self.marionette = marionette
        self.conf = conf
        self.env = env
        self.marionette = marionette
        self.puppeteer = puppeteer

    def wait_for_element_displayed(self, by, locator, timeout=20):
        Wait(self.marionette, timeout,
             ignored_exceptions=[NoSuchElementException, StaleElementException])\
            .until(lambda m: m.find_element(by, locator).is_displayed())
        return self.marionette.find_element(by, locator)

    def wait_for_element_enabled(self, element, timeout=10):
        Wait(self.marionette, timeout).until(
            lambda e: element.is_enabled(),
            message="Timed out waiting for element to be enabled"
        )

    def wait_for_element_exists(self, by, locator, timeout=20):
        Wait(self.marionette, timeout,
             ignored_exceptions=[NoSuchElementException, StaleElementException]) \
            .until(lambda m: m.find_element(by, locator))
        return self.marionette.find_element(by, locator)

    def wait_for_element_property_to_be_false(self, element, property, timeout=10):
        # XXX We have to switch between get_attribute and get_property here as the
        # content mode now required get_property for real properties of HTMLElements.
        # However, in some places (e.g. switch_to_chatbox), we're still operating in
        # a chrome mode. So we have to use get_attribute for these.
        # Bug 1277065 should fix this for marionette, alternately this should go
        # away when the e10s bug 1254132 is fixed.
        def check_property(m):
            """
            if self.context == "content":
                return not element.get_property(property)
            """
            return element.get_attribute(property) == "false"

        Wait(self.marionette, timeout) \
            .until(check_property,
                   message="Timeout out waiting for " + property + " to be false")

    def get_chatbox_window_expr(self, expr):
        self.marionette.set_context("chrome")
        self.marionette.switch_to_frame()

        chatbox = self.wait_for_element_exists(By.TAG_NAME, 'chatbox')
        script = '''
            let chatBrowser = document.getAnonymousElementByAttribute(
              arguments[0], 'anonid',
              'content')

            // note that using wrappedJSObject waives X-ray vision, which
            // has security implications, but because we trust the code
            // running in the chatbox, it should be reasonably safe
            let chatGlobal = chatBrowser.contentWindow.wrappedJSObject;

            return chatGlobal.''' + expr

        return self.marionette.execute_script(script, [chatbox])

    def get_media_start_time(self):
        return self.get_chatbox_window_expr(
            "loop.conversation._sdkDriver._getTwoWayMediaStartTime()"
        )

    def get_media_start_time_uninitialized(self):
        return self.get_chatbox_window_expr(
            "loop.conversation._sdkDriver.CONNECTION_START_TIME_UNINITIALIZED"
        )

    def get_and_verify_room_url(self):
        button = self.wait_for_element_displayed(By.CLASS_NAME, "btn-copy")
        button.click()

        # click the element
        room_url = pyperclip.paste()

        return room_url

    def standalone_load_and_join_room(self, url):
        self.switch_to_standalone()
        self.marionette.navigate(url)

        # Join the room - the first time around, the tour will be displayed
        # so we look for its close button.
        join_button = self.wait_for_element_displayed(By.CLASS_NAME, "button-got-it")
        self.wait_for_element_enabled(join_button, 120)
        join_button.click()

    def switch_to_standalone(self):
        self.set_context("content")

    def set_context(self, context):
        self.context = context
        self.marionette.set_context(context)

    def check_video(self, selector):
        video = self.wait_for_element_displayed(By.CSS_SELECTOR, selector, 30)
        self.wait_for_element_property_to_be_false(video, "paused")
        self.wait_for_element_property_to_be_false(video, "ended")

    def send_chat_message(self, text):
        chatbox = self.wait_for_element_displayed(
            By.CSS_SELECTOR,
            ".text-chat-box > form > input"
        )

        chatbox.send_keys(text + "\n")

    def switch_to_chatbox(self):
        self.set_context("chrome")
        self.marionette.switch_to_frame()

        contentBox = "content"

        # Added time lapse to allow for DOM to catch up
        time.sleep(2)
        # XXX should be using wait_for_element_displayed, but need to wait
        # for Marionette bug 1094246 to be fixed.
        chatbox = self.wait_for_element_exists(By.TAG_NAME, 'chatbox')
        script = ("return document.getAnonymousElementByAttribute("
                  "arguments[0], 'anonid', '" + contentBox + "');")
        frame = self.marionette.execute_script(script, [chatbox])
        self.marionette.switch_to_frame(frame)
