from django.shortcuts import render
from django.utils.http import urlencode
from django.views.generic import ListView
from django.views.generic.edit import FormMixin
from .models import MeterData
from .forms.meter_filter_form import MeterFilterForm
from datetime import datetime

def home(request):
    return render(request, 'webapp/home.html')


class MeterDataView(FormMixin, ListView):
    title = 'MeterData'
    template_name = 'webapp/meterdata.html'
    model = MeterData
    context_object_name = 'meterdata'
    # ordering = ['-ReadAt']
    paginate_by = 10
    form_class = MeterFilterForm
    requestUrl = ''

    def get_queryset(self):
        data = self.model.objects.all()

        from_date = self.request.GET.get('fromDate', '')
        to_date = self.request.GET.get('toDate', '')
        meter_id = self.request.GET.get('meterId', 0)

        if from_date and from_date != '':
            try:
                dt_string = parse_date_to_iso(from_date)
                if dt_string != '':
                    data = data.filter(ReadAt__gte=dt_string)
                    self.requestUrl += '&fromDate=' + from_date
            except (ValueError, TypeError):
                pass

        if to_date and to_date != '':
            try:
                dt_string = parse_date_to_iso(to_date)
                if dt_string != '':
                    data = data.filter(ReadAt__lte=dt_string)
                    self.requestUrl += '&toDate=' + to_date
            except (ValueError, TypeError):
                pass

        if meter_id and meter_id != 0:
            try:
                data = data.filter(MeterId=meter_id)
                self.requestUrl += '&meterId=' + meter_id
            except ValueError:
                pass

        return data.order_by('-ReadAt')

    def get_context_data(self, **kwargs):
        context = super(MeterDataView, self).get_context_data(**kwargs)
        context['requestUrl'] = self.requestUrl
        from_date = self.request.GET.get('fromDate', '')
        to_date = self.request.GET.get('toDate', '')
        meter_id = self.request.GET.get('meterId', '')
        context['fromDate'] = from_date
        context['toDate'] = to_date
        context['meterId'] = meter_id

        return context


def parse_date_to_iso(date_str):
    date_str = date_str.replace("/", "-")
    datetime_format = ("%d-%m-%Y %H:%i:%s", "%d-%m-%Y %H:%M:%S", "%Y-%m-%d %H:%M:%S", "%d-%m-%Y", "%Y-%m-%dT%H:%M:%S.%fZ")
    for item in datetime_format:
        try:
            dt = datetime.strptime(date_str, item)
            to_iso = dt.isoformat()
            return to_iso
        except (ValueError, TypeError):
            continue

    return ''
