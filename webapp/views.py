from django.shortcuts import render
from django.views.generic import ListView
from django.core.paginator import Paginator
from .models import MeterData

def home(request):
    return render(request, 'webapp/home.html')

class MeterDataView(ListView):
    title = 'MeterData'
    model = MeterData
    template_name = 'webapp/meterdata.html'
    context_object_name = 'meterdata'
    ordering = ['-ReadAt']
    paginate_by = 10
    #paginated_orphans = 50
    #queryset = MeterData.objects.all()

    def get_context_data(self, **kwargs):
        context = super(MeterDataView, self).get_context_data(**kwargs)
        filter_set = MeterData.objects.all()

        #current_page = context.pop('page_obj', None)
        #context['current_page'] = current_page
        #context['ReadAt']
        return context
