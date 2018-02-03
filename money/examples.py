from django.http import HttpResponse
from django.db import connection
from django.shortcuts import render_to_response
from django.template import loader
from itertools import groupby
from calendar import month_name
import datetime
import time
import random
import datedelta

def demo_multibarchart(request):
    """
    multibarchart page
    """
    start_time = datetime.datetime(2017, 1, 1)
    nb_element = 7
    xdata = range(nb_element)
    xdata = list(map(lambda x: (start_time + datedelta.datedelta(months=x)).timestamp() * 1000, xdata))

    # nb_element = 100
    # start_time = int(time.mktime(datetime.datetime(2012, 6, 1).timetuple()) * 1000)
    # xdata = range(nb_element)
    # xdata = list(map(lambda x: start_time + x * 1000000000, xdata))
    ydata = [i + random.randint(1, 10) for i in range(nb_element)]
    ydata2 = list(map(lambda x: x * 2, ydata))

    tooltip_date = "%b %Y"
    extra_serie = {"tooltip": {"y_start": "There are ", "y_end": " calls"},
                   "date_format": tooltip_date}

    chartdata = {
        'x': xdata,
        'name1': 'series 1', 'y1': ydata, 'extra1': extra_serie,
        'name2': 'series 2', 'y2': ydata2, 'extra2': extra_serie,
    }

    charttype = "multiBarChart"
    chartcontainer = 'multibarchart_container'  # container name
    data = {
        'charttype': charttype,
        'chartdata': chartdata,
        'chartcontainer': chartcontainer,
        'extra': {
            'name': chartcontainer,
            'x_is_date': True,
            'x_axis_format': '%d %b %Y',
            'tag_script_js': True,
            'jquery_on_ready': True,
            'resize': True,
        },
    }
    return render_to_response('examples/multibarchart.html', data)


def demo_piechart(request):
    """
    pieChart page
    """
    xdata = ["Apple", "Apricot", "Avocado", "Banana", "Boysenberries",
             "Blueberries", "Dates", "Grapefruit", "Kiwi", "Lemon"]
    ydata = [52, 48, 160, 94, 75, 71, 490, 82, 46, 17]

    color_list = ['#5d8aa8', '#e32636', '#efdecd', '#ffbf00', '#ff033e', '#a4c639',
                  '#b2beb5', '#8db600', '#7fffd4', '#ff007f', '#ff55a3', '#5f9ea0']
    extra_serie = {
        "tooltip": {"y_start": "", "y_end": " cal"},
        # "color_list": color_list
    }
    chartdata = {'x': xdata, 'y1': ydata, 'extra1': extra_serie}
    charttype = "pieChart"
    chartcontainer = 'piechart_container'  # container name
    charts = [
        {
            'charttype': charttype,
            'chartdata': chartdata,
            'chartcontainer': chartcontainer,
            'extra': {
                'x_is_date': False,
                'x_axis_format': '',
                'tag_script_js': True,
                'jquery_on_ready': False,
            }
        },
    ]
    data = {
        'charts': charts
    }
    return render_to_response('examples/piechart.html', data)



def demo_linechart(request):
    """
    lineChart page
    """

    start_time = datetime.datetime(2017, 1, 1)
    nb_element = 7
    xdata = range(nb_element)
    xdata = list(map(lambda x: (start_time + datedelta.datedelta(months=x)).timestamp() * 1000, xdata))
    print(xdata)
    ydata = [1, 5, 20, 12, 23, 13, 2]
    ydata2 = [10, -5, 2, 12, 3, 83, 2]

    tooltip_date = "%d %b %Y %H:%M:%S %p"
    extra_serie1 = {
        "tooltip": {"y_start": "", "y_end": " cal"},
        "date_format": tooltip_date,
    }
    extra_serie2 = {
        "tooltip": {"y_start": "", "y_end": " cal"},
        "date_format": tooltip_date,
    }
    chartdata = {
        'x': xdata,
        'name1': 'series 1', 'y1': ydata, 'extra1': extra_serie1, 'kwargs1': {'color': '#a4c639'},
        'name2': 'series 2', 'y2': ydata2, 'extra2': extra_serie2, 'kwargs2': {'color': '#ff8af8'},
    }

    charttype = "lineChart"
    chartcontainer = 'linechart_container'  # container name
    data = {
        'charttype': charttype,
        'chartdata': chartdata,
        'chartcontainer': chartcontainer,
        'extra': {
            'x_is_date': True,
            'x_axis_format': '%d %b',
            'tag_script_js': True,
            'jquery_on_ready': False,
        }
    }
    return render_to_response('examples/linechart.html', data)
