from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^testcase/$', views.list_cases, name='list_cases'),
    url(r'^requirement/(?P<sysReq>[\w\-]+)/$', views.list_sysReq, name='sysReq'),
    url(r'^filename/(?P<filename>[\w\-]+).csv/$', views.list_filename, name='filename'),
    url(r'^testcase/(?P<testCaseId>[0-9]+)/$', views.test_case, name='test_case'),
]