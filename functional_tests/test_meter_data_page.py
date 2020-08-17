from datetime import timedelta

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from django.contrib.auth.models import User
from webapp.models import ServiceArea, Meter, MeterData
from django.utils import timezone
import time
import datetime


def create_meter_data():
    service_area = ServiceArea.objects.create(AreaId=1, AreaName='Test Area')
    print("Created Service Area")

    meter = Meter.objects.create(MeterId=1, AreaId=service_area)
    print("Created Meter")

    read_at = datetime.datetime(2020, 1, 1)
    for x in range(1, 50):
        MeterData.objects.create(ReadingId=x, MeterId=meter, ReadAt=read_at + timedelta(days=x), KWH=250.50*x, KW=0, KVA=0, KVAr=0,
                             Ph1i=0, Ph2i=0, Ph3i=0, Ph1v=0, Ph2v=0, Ph3v=0, PF=0)
    print("Created Meter Data")


class TestMeterDataPage(StaticLiveServerTestCase):

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
        super(TestMeterDataPage, self).setUp()

        create_meter_data()

        # create fake user
        test_user = User.objects.create(username='user')
        test_user.set_password('User*123')
        test_user.save()

        self.client.login(username='user', password='User*123')
        cookie = self.client.cookies['sessionid']
        self.browser.get(self.live_server_url)
        self.browser.add_cookie({'name': 'sessionid', 'value': cookie.value, 'secure': False, 'path': '/'})

    # Test meter data page
    def test_meter_data_page(self):
        read_from = datetime.datetime(2020, 1, 1)
        read_to = datetime.datetime(2020, 1, 31)

        self.browser.get(self.live_server_url)
        self.browser.implicitly_wait(5)
        self.browser.find_element_by_id('linkMeterDataPage').click()
        self.browser.find_element_by_id('meterId').send_keys('1')
        self.browser.find_element_by_id('fromDate').send_keys(read_from.strftime("%d/%m/%Y, %H:%M:%S"))
        self.browser.find_element_by_id('toDate').send_keys(read_to.strftime("%d/%m/%Y, %H:%M:%S"))

        self.browser.implicitly_wait(5)
        self.browser.find_element_by_class_name('btn-primary').click()
        try:
            WebDriverWait(self.browser, 7).until(lambda driver: driver.find_element_by_tag_name('body'))
            self.browser.implicitly_wait(5)
            next_btn = self.browser.find_element_by_class_name('page-link')
            self.assertIsNotNone(next_btn)
        except NoSuchElementException:
            self.assertTrue(False)
