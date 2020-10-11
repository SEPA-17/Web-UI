from django.db import models


class PredictionData(models.Model):
    predictionId = models.IntegerField(primary_key=True)
    AreaId = models.ForeignKey('ServiceArea', db_column='AreaId', on_delete=models.DO_NOTHING)
    prediction_date = models.DateTimeField()
    KWH = models.FloatField()
    minimum_KWH = models.FloatField()
    maximum_KWH = models.FloatField()
    predicted_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'prediction_table'
        unique_together = (('AreaId', 'prediction_date'),)
