from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import loader
from itertools import groupby
from calendar import month_name
from datetime import datetime
from decimal import Decimal
import datedelta
from django.contrib.auth.decorators import login_required
from money.dbs import *

@login_required
def index(request,
          year_str=str(datetime.date.today().year),
          mode="purchased"):

    year = int(year_str)

    def create_pie_charts(month, income_data, expense_data):

        xdata = list(map(lambda x: x['category_name'], expense_data))

        # make a total value positive
        ydata = list(map(lambda x: float(x['total']) * -1, expense_data))

        color_list = list(map(lambda x: x['category_color'], expense_data))

        total_expense = round(sum(ydata), 2)
        total_income = round(sum(list(map(lambda x: float(x['total']), income_data))), 2)

        extra_serie = {
            "tooltip": {"y_start": "$", "y_end": ""},
            "color_list": color_list
        }

        chart = {
            'id': 'pie-%s-%s' % (year, month),
            'month': month,
            'monthyear': '%s %s' % (month_name[month], year),
            'charttype': 'pieChart',
            'chartdata': {'x': xdata, 'y1': ydata, 'extra1': extra_serie},
            'chartcontainer': 'piechart_container_%s' % month,
            'extra': {
                'x_is_date': False,
                'x_axis_format': '',
                'tag_script_js': True,
                'jquery_on_ready': False,
            },

            'total_income': total_income,
            'total_expense': total_expense,
            'total_saving': total_income - total_expense
        }
        return chart

    def create_main_chart(sum_income_data, sum_expense_data):
        """
        bar chart displaying total income, total expense, and total saving in each month
        """
        """
            multibarchart page
            """
        start_time = datetime.datetime(year, 1, 1)
        xdata = range(len(sum_expense_data))
        xdata = list(map(lambda x: (start_time + datedelta.datedelta(months=x)).timestamp() * 1000, xdata))

        ydata1 = reversed(sum_income_data)
        ydata2 = reversed(sum_expense_data)

        tooltip_date = "%b %Y"
        extra_serie = {
            "tooltip": {"y_start": "$", "y_end": ""},
            "date_format": tooltip_date,
        }
        chartdata = {
            'x': xdata,
            'name1': 'Income', 'y1': ydata1, 'extra1': extra_serie,
            'name2': 'Expense', 'y2': ydata2, 'extra2': extra_serie,
        }

        chart = {
            'charttype': 'multiBarChart',
            'chartdata': chartdata,
            'chartcontainer': 'main_chart_container',
            'extra': {
                'x_is_date': True,
                'x_axis_format': '%b',
                'tag_script_js': True,
                'jquery_on_ready': True,
            },
        }
        return chart

    query_result = get_statement_summary(year, mode=mode)

    sum_income_data = []
    sum_expense_data = []

    pie_charts = []

    # create pie chart for all months
    year_data = {
        key: [row for row in group]
        for key, group in groupby(query_result, lambda row: row['c_month'])
    }
    for month, data in year_data.items():
        income_data = list(filter(lambda x: x['total'] > 0, data))
        expense_data = list(filter(lambda x: x['total'] < 0, data))

        sum_income_data.append(round(sum(list(map(lambda x: float(x['total']), income_data))), 2))
        sum_expense_data.append(round(sum(list(map(lambda x: float(x['total']) * -1, expense_data))), 2))

        pie_charts.append(create_pie_charts(month, income_data, expense_data))

    main_chart = create_main_chart(sum_income_data, sum_expense_data)

    total_income_now = sum(sum_income_data)
    total_expense_now = sum(sum_expense_data)

    annual_saving_goal = get_saving_goal(year)
    monthly_saving_goal = annual_saving_goal / 12
    expected_saving_now = datetime.date.today().month * monthly_saving_goal

    total_saving_now = total_income_now - total_expense_now
    actual_saving_percent = (Decimal(str(total_saving_now)) * 100) / expected_saving_now

    context = {
        'year': year,
        'mode': mode,
        'annual_saving_goal': annual_saving_goal,
        'monthly_saving_goal': round(monthly_saving_goal, 0),
        'expected_saving': expected_saving_now,
        'actual_saving_percent': actual_saving_percent,
        'available_years': get_record_years(),
        'total_income': total_income_now,
        'total_expense': total_expense_now,
        'total_saving': total_saving_now,
        'main_chart': main_chart,
        'pie_charts': pie_charts
    }

    template = loader.get_template('index.html')
    return HttpResponse(template.render(context, request))

    # return HttpResponse(year_data)


@login_required
def monthly_stmts(request,
                  year_str=str(datetime.date.today().year),
                  month_str=str(datetime.date.today().month),
                  mode="purchased"):
    year = int(year_str)
    month = int(month_str)
    details = get_statement_details(year, month, mode)
    context = {
        'date_display': '%s %s' % (month_name[month], year_str),
        'mode': mode,
        'stmt_details': details
    }
    print(details)
    template = loader.get_template('monthly_stmts.html')
    return HttpResponse(template.render(context, request))


