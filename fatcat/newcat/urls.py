from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^testcase/$', views.list_cases, name='list_cases'),
    url(r'^requirement/(?P<sysReq>[\w\-]+)/$', views.list_sysReq, name='sysReq'),
    url(r'^filename/(?P<filename>[\w\-]+).csv/$', views.list_filename, name='filename'),

    url(r'^testcase/(?P<testCaseId>[0-9]+)/$', views.test_case, name='test_case'),

    url(r'^testcase/(?P<testCaseId>[0-9]+)/edit/$', views.edit_testcase, name='edit_test_case'),
    url(r'^testcase/(?P<testCaseId>[0-9]+)/edit/steps/$', views.edit_teststeps, name='edit_test_steps'),
    url(r'^testcase/(?P<testCaseId>[0-9]+)/edit/assertions/$', views.edit_expected_results, name='edit_expected_results'),

    url(r'^create/$', views.create_testcase, name='create_testcase'),
    url(r'^create/group/$', views.create_testgroup, name='create_testgroup'),

    url(r'^$', views.index, name='index'),
    url(r'^close/$', views.close_window, name='close_window'),
]