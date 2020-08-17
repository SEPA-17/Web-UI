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
    paginate_by = 50
    requestUrl = {}

    def dispatch(self, request, *args, **kwargs):
        self.requestUrl['meterId'] = self.request.GET.get('meterId', '')
        self.requestUrl['fromDate'] = self.request.GET.get('fromDate', '')
        self.requestUrl['toDate'] = self.request.GET.get('toDate', '')
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        data = self.model.objects.all()

        # Filters
        if self.requestUrl['meterId'] != 0:
            try:
                data = data.filter(meter_id=self.requestUrl['meterId'])
            except ValueError:
                pass

        if self.requestUrl['fromDate'] != '':
            try:
                dt_string = self.requestUrl['fromDate'].split('/')
                if len(dt_string) == 2:
                    data = data.filter(read_month__gte=dt_string[0])
                    data = data.filter(read_year__gte=dt_string[1])
            except (ValueError, TypeError):
                pass

        if self.requestUrl['toDate'] != '':
            try:
                dt_string = self.requestUrl['toDate'].split('/')
                if len(dt_string) == 2:
                    data = data.filter(read_month__lte=dt_string[0])
                    data = data.filter(read_year__lte=dt_string[1])
            except (ValueError, TypeError):
                pass

        return data.order_by('meter_id', '-read_year', '-read_month')

    def get_context_data(self, **kwargs):
        context = super(DataUsageView, self).get_context_data(**kwargs)
        context['requestUrl'] = urlencode(self.requestUrl)
        context['fromDate'] = self.requestUrl['fromDate']
        context['toDate'] = self.requestUrl['toDate']
        context['meterId'] = self.requestUrl['meterId']
        return context
