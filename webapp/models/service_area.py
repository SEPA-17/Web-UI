from django.db import models


class ServiceArea(models.Model):
    AreaId = models.AutoField(primary_key=True)
    AreaName = models.CharField(max_length=64)

    def __str__(self):
        return self.AreaName

    class Meta:
        db_table = "ServiceArea"
