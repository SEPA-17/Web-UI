import io

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

from webapp.models import PredictionData


@login_required
def prediction(request):
    _area_id = request.GET.get('areaid', 0)
    _year = request.GET.get('year', 2017)

    return render(request, 'webapp/graph/prediction.html', {'areaid': _area_id, 'year': _year})


# Render monthly image
def prediction_png(request):
    # time.sleep(3)

    _Area_id = 0
    if request.GET.get('areaid'):
        _area_id = request.GET['areaid']
    else:
        return graph_not_found()

    _year = request.GET.get('year', 2017)

    print(f"Request area id={_area_id}  year={_year}")

    data = PredictionData.objects.filter(AreaId_id=_area_id, prediction_date__year=_year).order_by('prediction_date', 'AreaId_id')
    if not data:
        return graph_not_found()

    print('test')
    month_data = data.values_list('prediction_date', 'kwh', 'minimum_KWH', 'maximum_KWH')

    months = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)
    monthly_usage = get_prediction(month_data)
    minimum_usage = get_prediction_min(month_data)
    maximum_usage = get_prediction_max(month_data)

    fig = Figure()
    ax = fig.add_subplot()

    ax.plot(months, minimum_usage, color='#7ec4ed', label='Minimum', linewidth=1.0)
    ax.plot(months, monthly_usage, marker='.', color='#2fa4e7', label='Usage', linewidth=2.0)
    ax.plot(months, maximum_usage, color='#1b597d', label='Maximum', linewidth=1.0)
    ax.set_xlim(1, 12)
    ax.set_xlabel('Months')
    ax.set_ylabel('KW')
    ax.set_title("Prediction KW")
    ax.grid()
    ax.legend(loc="upper right", shadow=True, bbox_to_anchor=(1, 1.075))
    canvas = FigureCanvas(fig)

    buf = io.BytesIO()
    canvas.print_png(buf)
    plt.close(fig)

    response = HttpResponse(buf.getvalue(), content_type='image/png')

    response['Content-Length'] = str(len(response.content))

    return response


def graph_not_found():
    with open("webapp/static/img/graph-no-data.png", "rb") as img_file:
        return HttpResponse(img_file.read(), content_type="image/png")


def get_prediction(values):
    # 12 months result
    result = [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00]
    for x in range(0, 12):
        for v in values:
            month = x + 1
            if month == v[0].month:
                result[x] = v[1]  # kwh
    return result


def get_prediction_min(values):
    # 12 months result
    result = [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00]
    for x in range(0, 12):
        for v in values:
            month = x + 1
            if month == v[0].month:
                result[x] = v[2]  # min kwh
    return result


def get_prediction_max(values):
    # 12 months result
    result = [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00]
    for x in range(0, 12):
        for v in values:
            month = x + 1
            if month == v[0].month:
                result[x] = v[3]  # max kwh
    return result
