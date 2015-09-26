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

import time
from six.moves import input

class TestLoopFxaContactCallHelper(MarionetteTestCase):

	def setUp(self):
		MarionetteTestCase.setUp(self)

		self.marionette.enforce_gecko_prefs(FIREFOX_PREFERENCES)

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


	def remote_join_room(self, room_url):
		# navigate to the given room
		self.marionette.navigate(room_url)
		
		# join the conversation
		self.marionette.set_context("content")
		join_button = self.wait_for_element_displayed(By.CLASS_NAME, "btn-join", 10)

		join_button.click()



	def test_browser_call_recipient(self):
		room_url = input("The chat room url is:")

		self.remote_join_room(room_url)

		done = input("Done?")


	def tearDown(self):
		MarionetteTestCase.tearDown(self)
