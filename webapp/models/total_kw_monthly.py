from django.db import models


class TotalKwMonthly(models.Model):
    meter_id = models.IntegerField(primary_key=True)
    read_month = models.IntegerField()
    read_year = models.IntegerField()
    total_kw = models.DecimalField(max_digits=19, decimal_places=4)

    class Meta:
        managed = False
        db_table = 'vw_total_kw_monthly'
