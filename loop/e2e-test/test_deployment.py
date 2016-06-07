import pytest
import time
import urlparse
from helpers import Helpers
from marionette_driver.by import By


@pytest.mark.usefixtures('conf', 'env', 'marionette', 'puppeteer')
class TestBrowserCall(Helpers):
    @pytest.fixture(autouse=True)
    def setUp(self, conf, env, marionette, puppeteer):
        self.env = env
        self.conf = conf
        self.marionette = marionette
        self.marionette.set_context("chrome")
        self.puppeteer = puppeteer
        Helpers.setUp(self, self.conf, self.env, self.marionette, self.puppeteer)
        self.firefox_preferences = {
            "loop.server": "%s/v0" % self.conf.get(env, 'loop_server'),
            "loop.linkClicker.url": "https://invalid/",
            "loop.gettingStarted.latestFTUVersion": 2,
            "loop.remote.autostart": True,
        }

    def test_browser_call(self):
        # Load the home page and set some preferences
        self.set_context('content')
        self.marionette.navigate("about:home")
        self.marionette.set_prefs(self.firefox_preferences)

        # Open the panel to share
        self.set_context("chrome")
        self.marionette.switch_to_frame()
        button = self.marionette.find_element(By.ID, "loop-button")
        button.click()

        # Switch to the panel
        frame = self.marionette.find_element(By.ID, "loop-panel-iframe")
        self.marionette.switch_to_frame(frame)

        # Start a local conversation
        button = self.wait_for_element_displayed(
            By.CSS_SELECTOR, ".new-room-view .btn-info"
        )
        self.wait_for_element_enabled(button, 120)
        button.click()

        # Close the share panel
        copyLink = self.wait_for_element_displayed(By.CLASS_NAME, "btn-copy")
        self.wait_for_element_enabled(copyLink, 120)
        copyLink.click()

        # Check the self video in the conversation window
        self.set_context("chrome")
        self.marionette.switch_to_frame()

        # Added time lapse to allow for DOM to catch up
        time.sleep(2)
        chatbox = self.wait_for_element_exists(By.TAG_NAME, 'chatbox')
        script = ("return document.getAnonymousElementByAttribute("
                  "arguments[0], 'anonid', 'content');")
        frame = self.marionette.execute_script(script, [chatbox])
        self.marionette.switch_to_frame(frame)

        # expect a video container on desktop side
        media_container = self.wait_for_element_displayed(
            By.CLASS_NAME, "media-layout"
        )
        assert media_container.tag_name == "div"

        video = self.wait_for_element_displayed(
            By.CSS_SELECTOR, ".local-video", 30
        )
        self.wait_for_element_property_to_be_false(video, "paused")
        self.wait_for_element_property_to_be_false(video, "ended")

        # Make sure that the media start time is not initialized
        start_time = self.get_media_start_time()
        unitialized_start_time = self.get_media_start_time_uninitialized()
        assert start_time == unitialized_start_time

        chatbox = self.wait_for_element_exists(By.TAG_NAME, 'chatbox')
        script = ("return document.getAnonymousElementByAttribute("
                  "arguments[0], 'anonid', 'content');")
        frame = self.marionette.execute_script(script, [chatbox])
        self.marionette.switch_to_frame(frame)
        room_url = self.get_and_verify_room_url()
        assert urlparse.urlparse(room_url).scheme in ['http', 'https']

        # load the link clicker interface into the current content browser
        self.set_context('content')
        self.marionette.navigate(room_url)

        # Join the room - the first time around, the tour will be displayed
        # so we look for its close button.
        join_button = self.wait_for_element_displayed(By.CLASS_NAME, "button-got-it")
        self.wait_for_element_enabled(join_button, 120)
        join_button.click()

        # Check we get the video streams
        self.switch_to_standalone()
        self.check_video(".remote-video")
        self.switch_to_chatbox()
        self.check_video(".remote-video")

        # Check text messaging
        self.switch_to_chatbox()
        self.send_chat_message("test1")

        # Now check the result on the link clicker.
        self.switch_to_standalone()
        text_entry = self.wait_for_element_displayed(
            By.CSS_SELECTOR,
            ".text-chat-entry.received > p"
        )
        assert text_entry.text == "test1"

        # Then send a message using the standalone.
        self.send_chat_message("test2")

        # Finally check the link generator got it.
        self.switch_to_chatbox()
        text_entry = self.wait_for_element_displayed(
            By.CSS_SELECTOR,
            ".text-chat-entry.received > p"
        )
        assert text_entry.text == "test2"

        # since bi-directional media is connected, make sure we've set
        # the start time
        # Make sure that the media start time is not initialized
        start_time = self.get_media_start_time()
        unitialized_start_time = self.get_media_start_time_uninitialized()
        assert start_time != unitialized_start_time

        # Check that screenshare was automatically started
        self.switch_to_standalone()
        self.check_video(".screen-share-video")

        # We hangup on the remote (standalone) side, because this also leaves
        # the local chatbox with the local publishing media still connected,
        # which means that the local_check_connection_length below
        # verifies that the connection is noted at the time the remote media
        # drops, rather than waiting until the window closes.
        self.switch_to_standalone()
        button = self.marionette.find_element(By.CLASS_NAME, "btn-hangup")
        button.click()
        self.switch_to_chatbox()
        self.wait_for_element_displayed(By.CLASS_NAME, "room-invitation-content")

        # Check that we had more than one noted call
        noted_calls = self.get_chatbox_window_expr(
            "loop.conversation._sdkDriver._connectionLengthNotedCalls"
        )
        assert noted_calls > 0

        # Hangup on local will open feedback window first
        self.set_context("chrome")
        self.marionette.switch_to_frame()
        chatbox = self.wait_for_element_exists(By.TAG_NAME, 'chatbox')
        close_button = chatbox.find_element(By.ANON_ATTRIBUTE, {"class": "chat-loop-hangup chat-toolbarbutton"})
        close_button.click()
        self.switch_to_chatbox()
        feedbackPanel = self.wait_for_element_displayed(
            By.CSS_SELECTOR, ".feedback-view-container"
        )
        assert feedbackPanel != ""

        # Close the window once again to see the rename layout
        self.set_context("chrome")
        self.marionette.switch_to_frame()
        chatbox = self.wait_for_element_exists(By.TAG_NAME, 'chatbox')
        close_button = chatbox.find_element(By.ANON_ATTRIBUTE, {"class": "chat-loop-hangup chat-toolbarbutton"})
        close_button.click()

        self.set_context("chrome")
        frame = self.marionette.find_element(
            By.ID,
            "loop-panel-iframe"
        )
        self.marionette.switch_to_frame(frame)
        renameInput = self.wait_for_element_displayed(By.CSS_SELECTOR, ".rename-input")
        assert renameInput != ""
