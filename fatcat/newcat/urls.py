from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^testcase/$', views.list_cases, name='list_cases'),
    url(r'^requirement/(?P<sysReq>[\w\-]+)/$', views.list_sysReq, name='sysReq'),
    url(r'^filename/(?P<filename>[\w\-]+).csv/$', views.list_filename, name='filename'),
    url(r'^testcase/(?P<testCaseId>[0-9]+)/$', views.test_case, name='test_case'),
    url(r'^create/$', views.create_testcase, name='create_testcase'),
    url(r'^create/group/$', views.create_testgroup, name='create_testgroup'),
    url(r'^close/$', views.close_window, name='close_window'),
]