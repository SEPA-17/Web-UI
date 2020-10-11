from urllib.parse import urlencode
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from ..models import PredictionData


class PredictionView(ListView):
    title = 'Prediction Data'
    template_name = 'webapp/prediction_data.html'
    model = PredictionData
    context_object_name = 'prediction_data'
    paginate_by = 50
    requestUrl = {}

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.requestUrl['areaId'] = self.request.GET.get('areaId', '')
        self.requestUrl['year'] = self.request.GET.get('year', '')
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        data = self.model.objects.only('AreaId', 'predicted_at', 'minimum_KWH', 'KWH', 'maximum_KWH', 'prediction_date')
        raw_sql = "SELECT DISTINCT MAX(predictionId) AS predictionId FROM prediction_table WHERE predictionId > 0"

        # Filters
        if self.requestUrl['areaId'] and self.requestUrl['areaId'] != 0:
            try:
                area_id = self.requestUrl['areaId']
                data = data.filter(AreaId=area_id)
                raw_sql = raw_sql + " AND AreaId = " + area_id + ""
            except ValueError:
                pass

        if self.requestUrl['year'] and self.requestUrl['year'] != '' and len(self.requestUrl['year']) == 4:
            try:
                year = self.requestUrl['year']
                data = data.filter(prediction_date__year=year)
                raw_sql = raw_sql + " AND YEAR(prediction_date) = " + year + ""
            except (ValueError, TypeError):
                pass

        raw_sql = raw_sql + " GROUP BY AreaId, YEAR(prediction_date), MONTH(prediction_date)"
        #print(raw_sql)

        # Filter duplicate prediction data
        raw = self.model.objects.raw(raw_sql)
        ids = (obj.predictionId for obj in raw)
        data = data.filter(predictionId__in=ids)

        return data.order_by('AreaId', '-prediction_date').distinct()

    def get_context_data(self, **kwargs):
        context = super(PredictionView, self).get_context_data(**kwargs)
        context['requestUrl'] = urlencode(self.requestUrl)
        context['areaId'] = self.requestUrl['areaId']
        context['year'] = self.requestUrl['year']
        return context
