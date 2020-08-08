from urllib.parse import urlencode
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from ..models import MeterUsage
from ..helper import parse_date_to_iso

class DataUsageView(ListView):
    title = 'Data Usage'
    template_name = 'webapp/data_usage.html'
    model = MeterUsage
    context_object_name = 'datausage'
    paginate_by = 10
    requestUrl = {}

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        data = self.model.objects.all()
        return data.order_by('meter_id', '-read_year', '-read_month')
