from django.conf.urls import url

from . import views
from . import examples

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^report/annual-summary/(?P<year_str>\d{4})/(?P<mode>purchased|billed|due)$', views.index, name='report_annual_summary'),
    url(r'^report/monthly-stmts/(?P<year_str>\d{4})/(?P<month_str>\d+)/(?P<mode>purchased|billed|due)$', views.monthly_stmts, name='report_monthly_stmts'),
    url(r'^piechart/', examples.demo_piechart, name='demo_piechart'),
    url(r'^linechart/', examples.demo_linechart, name='demo_linechart'),
    url(r'^multibarchart/', examples.demo_multibarchart, name='demo_multibarchart'),
]