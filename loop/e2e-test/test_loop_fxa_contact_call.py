from marionette_driver.by import By
from marionette_driver.errors import NoSuchElementException, StaleElementException
# noinspection PyUnresolvedReferences
from marionette_driver import Wait
from marionette import MarionetteTestCase

import os
import sys
import urlparse
sys.path.insert(1, os.path.dirname(os.path.abspath(__file__)))

from config import *

import pyperclip
import time
from six.moves import input


class TestLoopFxaContactCall(MarionetteTestCase):

	def setUp(self):
		MarionetteTestCase.setUp(self)
		self.marionette.enforce_gecko_prefs(FIREFOX_PREFERENCES)
		self.marionette.set_context("chrome")

	def switch_to_panel(self):
		hello_button = self.marionette.find_element(By.ID, "loop-button")
		hello_button.click()

		frame = self.marionette.find_element(By.ID, "loop-panel-iframe")
		self.marionette.switch_to_frame(frame)

	def switch_to_chatbox(self):
		self.marionette.set_context("chrome")
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
	    Wait(self.marionette, timeout,
	         ignored_exceptions=[NoSuchElementException, StaleElementException]) \
	        .until(lambda m: m.find_element(by, locator))
	    return self.marionette.find_element(by, locator)

	def wait_for_element_enabled(self, element, timeout=10):
		Wait(self.marionette, timeout) \
			.until(lambda e: element.is_enabled(),
				message="Timed out waiting for element to be enabled")

	def local_start_a_conversation(self):
		button = self.marionette.find_element(By.CSS_SELECTOR, ".rooms .btn-info")

		self.wait_for_element_enabled(button, 120)

		button.click()

	def local_get_and_verify_room_url(self):
		self.switch_to_chatbox()
		# should wait for char box to show instead of sleeping once
		time.sleep(5)
		button = self.wait_for_element_displayed(By.CLASS_NAME, "btn-copy")
		self.wait_for_element_enabled(button)
		button.click()
		room_url = pyperclip.paste()
		self.assertIn(urlparse.urlparse(room_url).scheme, ['http', 'https'],
						"room URL returned by server: '" + room_url +
						"' has invalid scheme")
		return room_url

	def local_get_chatbox_window_expr(self, expr):
	    """
	    :expr: a sub-expression which must begin with a property of the
	    global content window (e.g. "location.path")

	    :return: the value of the given sub-expression as evaluated in the
	    chatbox content window
	    """
	    self.marionette.set_context("chrome")
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
			"loop.conversation._sdkDriver._getTwoWayMediaStartTime()")

	def local_get_media_start_time_uninitialized(self):
		return self.local_get_chatbox_window_expr(
			"loop.conversation._sdkDriver.CONNECTION_START_TIME_UNINITIALIZED")

	def local_check_media_start_time_uninitialized(self):
		print(self.local_get_media_start_time())
		print(self.local_get_media_start_time_uninitialized())
		self.assertEqual(
			self.local_get_media_start_time(),
			self.local_get_media_start_time_uninitialized(),
			"media start time should not be initialized before link clicker enters room")

	def test_browser_call_caller(self):
		self.switch_to_panel()

		self.local_start_a_conversation()

		#self.local_check_media_start_time_uninitialized() None - -1

		room_url = self.local_get_and_verify_room_url()
		print("The room url is: " + room_url)
		joined = input("Give a GO sign")

	def tearDown(self):
		MarionetteTestCase.tearDown(self)
