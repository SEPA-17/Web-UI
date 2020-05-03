from django.db import models
from . import service_area


class Meter(models.Model):
    MeterId = models.AutoField(primary_key=True)
    AreaId = models.ForeignKey(service_area.ServiceArea, db_column='AreaId', on_delete=models.SET_NULL, blank=True,
                               null=True)

    def __str__(self):
        return self.MeterId

    class Meta:
        db_table = "Meter"
