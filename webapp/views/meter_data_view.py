from urllib.parse import urlencode
from django.views.generic import ListView
from django.views.generic.edit import FormMixin
from ..models import MeterData
from ..helper import parse_date_to_iso


class MeterDataView(FormMixin, ListView):
    title = 'MeterData'
    template_name = 'webapp/meterdata.html'
    model = MeterData
    context_object_name = 'meterdata'
    # ordering = ['-ReadAt']
    paginate_by = 10
    requestUrl = {}

    def dispatch(self, request, *args, **kwargs):
        self.requestUrl['meterId'] = self.request.GET.get('meterId', '')
        self.requestUrl['fromDate'] = self.request.GET.get('fromDate', '')
        self.requestUrl['toDate'] = self.request.GET.get('toDate', '')
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        data = self.model.objects.all()

        if self.requestUrl['meterId'] != 0:
            try:
                data = data.filter(MeterId=self.requestUrl['meterId'])
            except ValueError:
                pass

        if self.requestUrl['fromDate'] != '':
            try:
                dt_string = parse_date_to_iso(self.requestUrl['fromDate'])
                if dt_string != '':
                    data = data.filter(ReadAt__gte=dt_string)
            except (ValueError, TypeError):
                pass

        if self.requestUrl['toDate'] != '':
            try:
                dt_string = parse_date_to_iso(self.requestUrl['toDate'])
                if dt_string != '':
                    data = data.filter(ReadAt__lte=dt_string)
            except (ValueError, TypeError):
                pass

        return data.order_by('-ReadAt')

    def get_context_data(self, **kwargs):
        context = super(MeterDataView, self).get_context_data(**kwargs)
        context['requestUrl'] = urlencode(self.requestUrl)
        context['fromDate'] = self.requestUrl['fromDate']
        context['toDate'] = self.requestUrl['toDate']
        context['meterId'] = self.requestUrl['meterId']
        return context
