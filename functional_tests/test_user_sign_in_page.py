from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from django.contrib.auth.models import User
import time


class TestUserSignInPage(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.browser = webdriver.Chrome('functional_tests/chromedriver.exe')
        cls.browser.maximize_window()

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super().tearDownClass()

    def setUp(self):
        super(TestUserSignInPage, self).setUp()

        # create fake user
        test_user = User.objects.create(username='user')
        test_user.set_password('User*123')
        test_user.save()

    # User request page for first time should require login page
    def test_should_require_sign_in(self):
        self.browser.get(self.live_server_url)
        login_form = self.browser.find_element_by_id('login-form')
        self.assertIsNotNone(login_form)

    # User should sign in successfully
    def test_sign_in_with_user_should_success(self):
        self.browser.get(self.live_server_url + reverse('login'))
        self.browser.find_element_by_id('id_username').send_keys('user')
        self.browser.find_element_by_id('id_password').send_keys('User*123')
        self.browser.find_element_by_class_name('btn-primary').click()

        try:
            WebDriverWait(self.browser, 7).until(lambda driver: driver.find_element_by_tag_name('body'))
            home_screen = self.browser.find_element_by_class_name('home-icon-group')
            time.sleep(10)
            self.assertTrue(home_screen is not None)
        except NoSuchElementException:
            self.assertTrue(False)
