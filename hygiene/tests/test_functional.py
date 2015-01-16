import shutil
import unittest

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import override_settings

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

from . import factories


@unittest.skipUnless(shutil.which('phantomjs'), 'PhantomJS is not installed')
@override_settings(COMPRESS_PRECOMPILERS=(('text/less', 'lessc {infile} {outfile}'), ))
class FunctionalTests(StaticLiveServerTestCase):
    """Iteractive tests with selenium."""

    @classmethod
    def setUpClass(cls):
        cls.browser = webdriver.PhantomJS()
        super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super().tearDownClass()

    def setUp(self):
        self.username = 'test'
        self.password = 'test'
        factories.UserFactory.create(username=self.username, password=self.password)

    def test_show_login(self):
        """The login should be shown on page load."""

        self.browser.get(self.live_server_url)
        form = self.browser.find_element_by_id('login')
        self.assertTrue(form.is_displayed(), 'Login form should be visible.')
        collect = self.browser.find_element_by_id('collect')
        self.assertFalse(collect.is_displayed(), 'Question form should not be visible.')
        results = self.browser.find_element_by_id('results')
        self.assertFalse(results.is_displayed(), 'Results should not be visible.')

    def login(self, username, password):
        """Helper for login form submission."""

        self.browser.get(self.live_server_url)
        form = self.browser.find_element_by_id('login')
        username_input = form.find_element_by_name('username')
        username_input.send_keys(username)
        password_input = form.find_element_by_name('password')
        password_input.send_keys(password)
        form.submit()

    def test_login(self):
        """Submit the login form with a valid login."""

        self.login(self.username, self.password)
        WebDriverWait(self.browser, 5).until(
            expected_conditions.visibility_of_element_located((By.ID, 'collect')))
        form = self.browser.find_element_by_id('login')
        self.assertFalse(form.is_displayed(), 'Login form should no longer be visible.')

    def test_invalid_login(self):
        """Submit the login form with an invalid login."""

        self.login(self.username, self.password[1:])
        error = WebDriverWait(self.browser, 5).until(
            expected_conditions.presence_of_element_located((By.CLASS_NAME, 'error')))
        self.assertEqual('Invalid username/password', error.text)
        form = self.browser.find_element_by_id('login')
        self.assertTrue(form.is_displayed(), 'Login form should still be visible.')
