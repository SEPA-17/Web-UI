from django.db import models


class MeterUsage(models.Model):
    meter_id = models.IntegerField(primary_key=True)
    read_month = models.IntegerField()
    read_year = models.IntegerField()
    min_kwh = models.DecimalField(max_digits=19, decimal_places=4)
    max_kwh = models.DecimalField(max_digits=19, decimal_places=4)
    total_usage = models.DecimalField(max_digits=19, decimal_places=4)

    class Meta:
        managed = False
        db_table = 'vw_meter_usage'
