import time
import io

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

from webapp.models.meter_usage import MeterUsage


# Render page
@login_required
def monthly(request):
    _meter_id = request.GET.get('meterid', 0)
    _year = request.GET.get('year', 2017)
    # print(f"Request meter id={_meter_id}  year={_year}")
    return render(request, 'webapp/graph/monthly.html', {'meterid': _meter_id, 'year': _year})


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

    data = MeterUsage.objects.filter(meter_id=_meter_id, read_year=_year).order_by('read_year', 'read_month')
    if not data:
        return graph_not_found()

    month_kw = data.values_list('read_month', 'total_usage')
    # month, kw = zip(*month_kw)
    months = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)
    monthly_usage = get_usage(month_kw)

    fig = Figure()
    ax = fig.add_subplot()

    ax.plot(months, monthly_usage, marker='.', color='#2fa4e7', label='Usage')
    #plt.xticks(months)
    ax.set_xlim(1, 12)
    ax.set_xlabel('Months')
    ax.set_ylabel('KW')
    ax.set_title("Zodicom KW")
    ax.grid()
    ax.legend(loc="upper right", shadow=True, bbox_to_anchor=(1, 1.075))
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


def get_usage(values):
    # 12 months result
    result = [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00]
    for x in range(0, 12):
        for v in values:
            month = x + 1
            if month == v[0]:
                result[x] = v[1]
    return result
