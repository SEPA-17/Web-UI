from datetime import date
from urllib.parse import urlencode
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from ..models import MeterUsage


class DataUsageView(ListView):
    title = 'Data Usage'
    template_name = 'webapp/data_usage.html'
    model = MeterUsage
    context_object_name = 'datausage'
    paginate_by = 50
    requestUrl = {}

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.requestUrl['meterId'] = self.request.GET.get('meterId', 0)
        self.requestUrl['fromMonth'] = self.request.GET.get('fromMonth', '0')
        self.requestUrl['fromYear'] = self.request.GET.get('fromYear', '0')
        self.requestUrl['toMonth'] = self.request.GET.get('toMonth', 0)
        self.requestUrl['toYear'] = self.request.GET.get('toYear', 0)
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        data = self.model.objects.all()

        # Filters
        if self.requestUrl['meterId'] != 0:
            try:
                data = data.filter(meter_id=self.requestUrl['meterId'])
            except ValueError:
                pass

        try:
            from_month = int(self.requestUrl['fromMonth'])
            from_year = int(self.requestUrl['fromYear'])
            # print(f'from month: {from_month} from year: {from_year}')
            if from_month > 0 and from_year > 0:
                data = data.filter(read_month__gte=from_month)
                data = data.filter(read_year__gte=from_year)
        except (ValueError, TypeError) as e:
            pass

        try:
            to_month = int(self.requestUrl['toMonth'])
            to_year = int(self.requestUrl['toYear'])
            # print(f'to month: {to_month} to year: {to_year}')
            if to_month > 0 and to_year > 0:
                data = data.filter(read_month__lte=to_month)
                data = data.filter(read_year__lte=to_year)
        except (ValueError, TypeError):
            pass

        return data.order_by('meter_id', '-read_year', '-read_month')

    def get_context_data(self, **kwargs):
        context = super(DataUsageView, self).get_context_data(**kwargs)
        context['requestUrl'] = urlencode(self.requestUrl)
        context['meterId'] = self.requestUrl['meterId']
        context['fromMonth'] = int(self.requestUrl['fromMonth'])
        context['fromYear'] = int(self.requestUrl['fromYear'])
        context['toMonth'] = int(self.requestUrl['toMonth'])
        context['toYear'] = int(self.requestUrl['toYear'])

        current_date = date.today()
        context['monthRange'] = range(1, 13)
        context['yearRange'] = range(current_date.year - 10, current_date.year + 10)
        return context
