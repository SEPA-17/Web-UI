import datetime
import io
from django.shortcuts import render
from django.http import HttpResponse
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.dates import DateFormatter
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

from webapp.models.total_kw_monthly import TotalKwMonthly

def monthly(request):
    return render(request, 'webapp/graph/monthly.html')

def monthly_png(request):

    meterid = 98801006
    year = 2017

    data = TotalKwMonthly.objects.filter(meter_id=meterid, read_year=year).order_by('read_year', 'read_month')

    month_kw = data.values_list('read_month', 'total_kw')
    month, kw = zip(*month_kw)

    fig = Figure()
    ax = fig.add_subplot()

    ax.plot(month, kw, marker='.', color='#0000ff', label='Month Kw')
    #ax.plot(month, kw, marker='.', color='#0000ff', label='')

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


def monthly_png_v1(request):
    meterid = 98801006
    year = 2017

    data = TotalKwMonthly.objects.filter(meter_id=meterid, read_year=year).order_by('read_year', 'read_month')

    month_kw = data.values_list('read_month', 'total_kw')
    month, kw = zip(*month_kw)

    fig = Figure()
    ax = fig.add_subplot()

    ax.plot(month, kw, 'ro')
    ax.plot(month, kw, 'b-')

    ax.set_xlabel('Month')
    ax.set_ylabel('Kw')
    ax.set_title("Zodicom Kw")
    ax.grid()

    canvas = FigureCanvas(fig)

    buf = io.BytesIO()
    canvas.print_png(buf)
    plt.close(fig)

    response = HttpResponse(buf.getvalue(), content_type='image/png')

    response['Content-Length'] = str(len(response.content))

    return response


def monthly_bck(request):

    fig = plt.figure()
    canvas = FigureCanvas(fig)

    x = [100, 200, 300, 200]
    y = [1.5, 2, 3, 4]

    plt.plot(x, y)

    #ax = fig.add_subplot(111)
    #ax.plot([1, 2, 3])

    #response = django.http.HttpResponse(content_type='image/jpg')
    #canvas.print_figure(response)

    plt.xlabel("Month")
    plt.ylabel("Kw")
    plt.legend()
    plt.grid(True)

    buf = io.BytesIO()
    canvas.print_png(buf)
    plt.close(fig)

    response = HttpResponse(buf.getvalue(), content_type='image/png')

    response['Content-Length'] = str(len(response.content))

    return response

def yearly(request):
    return render(request, 'webapp/graph/yearly.html')
