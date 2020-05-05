from django.db import models
from django.utils import timezone
from . import meter


class MeterData(models.Model):
    ReadingId = models.AutoField(primary_key=True)
    MeterId = models.ForeignKey(meter.Meter, db_column='MeterId', on_delete=models.SET_NULL, blank=True, null=True)
    ReadAt = models.DateTimeField(default=timezone.now)
    KWH = models.FloatField()
    KW = models.FloatField()
    KVA = models.FloatField()
    KVAr = models.FloatField()
    Ph1i = models.FloatField()
    Ph2i = models.FloatField()
    Ph3i = models.FloatField()
    Ph1v = models.FloatField()
    Ph2v = models.FloatField()
    Ph3v = models.FloatField()
    PF = models.FloatField()

    def __str__(self):
        return self.ReadingId + ',' + self.MeterId + ',' + self.ReadAt + ',' + self.KWH + ',' + self.KW + ',' + self.KVA + ',' + self.KVAr + ',' + self.Ph1i + ',' + self.Ph2i + ',' + self.Ph3i + ',' + self.Ph1v + ',' + self.Ph2v + ',' + self.Ph3v + ',' + self.PF

    class Meta:
        db_table = "MeterData"
