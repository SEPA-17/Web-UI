import time
import io

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

from webapp.models.total_kw_monthly import TotalKwMonthly


# Render page
@login_required
def monthly(request):
    _meter_id = request.GET.get('meterid', 0)
    _year = request.GET.get('year', 2017)
    return render(request, 'webapp/graph/monthly.html', {'meterId': _meter_id, 'year': _year})


# Render monthly image
def monthly_png(request):
    # time.sleep(3)

    _meter_id = 0
    if request.GET.get('meterId'):
        _meter_id = request.GET['meterId']
    else:
        return graph_not_found()

    _year = request.GET.get('year', 2017)

    # print(f"Request meter id={_meter_id}  year={_year}")

    data = TotalKwMonthly.objects.filter(meter_id=_meter_id, read_year=_year).order_by('read_year', 'read_month')
    if not data:
        return graph_not_found()

    month_kw = data.values_list('read_month', 'total_kw')
    month, kw = zip(*month_kw)

    fig = Figure()
    ax = fig.add_subplot()

    ax.plot(month, kw, marker='.', color='#0000ff', label='Month Kw')
    # ax.plot(month, kw, marker='.', color='#0000ff', label='')

    ax.set_xlabel('Month')
    ax.set_ylabel('Kw')
    ax.set_title("Zodicom Kw")
    ax.grid()
    ax.legend()

    canvas = FigureCanvas(fig)

    buf = io.BytesIO()
    canvas.print_png(buf)
    plt.close(fig)

    response = HttpResponse(buf.getvalue(), content_type='image/png')

    response['Content-Length'] = str(len(response.content))

    return response


def yearly(request):
    return render(request, 'webapp/graph/yearly.html')


def graph_not_found():
    with open("webapp/static/img/graph-no-data.png", "rb") as img_file:
        return HttpResponse(img_file.read(), content_type="image/png")
