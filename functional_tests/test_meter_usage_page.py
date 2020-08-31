from django.db import connection
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.models import User
from webapp.models import MeterUsage
import datetime


def create_meter_usage():
    read_month = 1
    read_year = 2020

    with connection.schema_editor() as schema_editor:
        schema_editor.create_model(MeterUsage)

    for x in range(1, 50):
        MeterUsage.objects.create(meter_id=x, read_month=read_month, read_year=read_year, min_kwh=0, max_kwh=200, total_usage=200)
        read_month = read_month + 1
        if read_month > 12:
            read_month = 1
            read_year = read_year + 1
    print("Created Data usage")


def delete_meter_usage():
    with connection.schema_editor() as schema_editor:
        schema_editor.delete_model(MeterUsage)


class TestDataUsagePage(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.browser = webdriver.Chrome('functional_tests/chromedriver.exe')
        cls.browser.maximize_window()

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super().tearDownClass()
        delete_meter_usage()

    def setUp(self):
        super(TestDataUsagePage, self).setUp()

        create_meter_usage()

        # create fake user
        test_user = User.objects.create(username='user')
        test_user.set_password('User*123')
        test_user.save()

        # login
        self.client.login(username='user', password='User*123')
        cookie = self.client.cookies['sessionid']
        self.browser.get(self.live_server_url)
        self.browser.add_cookie({'name': 'sessionid', 'value': cookie.value, 'secure': False, 'path': '/'})

    # Test data usage page
    def test_data_usage_page(self):
        read_from = datetime.datetime(2020, 1, 1)
        read_to = datetime.datetime(2020, 1, 30)

        self.browser.get(self.live_server_url + "/datausage")
        # WebDriverWait(self.browser, 7).until(lambda driver: driver.find_element_by_tag_name('body'))
        # self.browser.find_element_by_id('linkDataUsagePage').click()
        WebDriverWait(self.browser, 7).until(lambda driver: driver.find_element_by_tag_name('body'))
        self.browser.find_element_by_id('meterId').send_keys('1')
        self.browser.find_element_by_id('fromDate').send_keys(read_from.strftime("%m/%Y"))
        self.browser.find_element_by_id('toDate').send_keys(read_to.strftime("%m/%Y"))

        self.browser.find_element_by_class_name('btn-primary').click()
        try:
            WebDriverWait(self.browser, 7).until(lambda driver: driver.find_element_by_tag_name('body'))
            record_found = self.browser.find_element_by_id('recordFound')
            self.assertIsNotNone(record_found)
        except NoSuchElementException:
            self.assertTrue(False)
