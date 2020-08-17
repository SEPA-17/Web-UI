from django.utils import timezone

from django.test import TestCase
from webapp.models import ServiceArea, Meter, MeterData


class MeterDataTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        area_id = 1
        meter_id = '000001'

        service_area = ServiceArea.objects.create(AreaId=area_id, AreaName='Test Area')
        print("Created Service Area")

        meter = Meter.objects.create(MeterId=meter_id, AreaId=service_area)
        print("Created Meter")

        MeterData.objects.create(ReadingId=1, MeterId=meter, ReadAt=timezone.now(), KWH=250.50, KW=0, KVA=0, KVAr=0, Ph1i=0, Ph2i=0, Ph3i=0, Ph1v=0, Ph2v=0, Ph3v=0, PF=0)
        print("Created Meter Data")

    def test_meter_date_is_created(self):
        self.assertTrue(MeterData.objects.all().count() > 0)