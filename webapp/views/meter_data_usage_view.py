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
                dt_string = parse_date_to_iso(self.requestUrl['fromDate'])
                if dt_string != '':
                    data = data.filter(read_at__gte=dt_string)
            except (ValueError, TypeError):
                pass

        if self.requestUrl['toDate'] != '':
            try:
                dt_string = parse_date_to_iso(self.requestUrl['toDate'])
                if dt_string != '':
                    data = data.filter(read_at__lte=dt_string)
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
