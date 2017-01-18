from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^testcase/$', views.list_cases, name='list_cases'),
    url(r'^filename/(?P<filename>[\w\-]+).csv/$', views.list_filename, name='filename'),
    url(r'^testcase/(?P<testCaseId>[0-9]+)/$', views.test_case, name='test_case'),

    url(r'^requirement/SR: (?P<sysReq>[\w\-]+)US: (?P<us>[\w\-]+)/$', views.list_sysReq, name='sysReq'),
    url(r'^requirement/SR: (?P<sysReq>[\w\-]+)US: (?P<us_endspace>[\w\-]+)/$', views.list_sysReq, name='sysReq'),
    url(r'^requirement/SR:(?P<sysReq>[\w\-]+)US:(?P<us_nospace>[\w\-]+)/$', views.list_sysReq, name='sysReq'),
    url(r'^requirement/SR: (?P<sysReq>[\w\-]+) / US: (?P<us_slashed>[\w\-]+)/$', views.list_sysReq, name='sysReq'),
    url(r'^requirement/SR: <EMPTY>US: (?P<us_EMPTY>[\w\-]+)/$', views.list_sysReq, name='sysReq'),
    url(r'^requirement/S-R: (?P<sysReq>[\w\-]+)  U-S: (?P<us_dashed>[\w\-]+)/$', views.list_sysReq, name='sysReq'),
    url(r'^requirement/SR (?P<sr_short>[\w\-]+)/$', views.list_sysReq, name='sysReq'),



    url(r'^requirement/User Story: (?P<us>[\w\-]+)/$', views.list_sysReq, name='sysReq'),
    url(r'^requirement/US (?P<us_short>[\w\-]+)/$', views.list_sysReq, name='sysReq'),
    url(r'^requirement/US: (?P<us_short_dotted>[\w\-]+)/$', views.list_sysReq, name='sysReq'),
    url(r'^requirement/US:(?P<us_nospace_inverse>[\w\-]+)SR:(?P<sysReq>[\w\-]+)/$', views.list_sysReq, name='sysReq'),
    url(r'^requirement/US: (?P<us_joined_inverse>[\w\-]+)SR: (?P<sysReq>[\w\-]+)/$', views.list_sysReq, name='sysReq'),
    url(r'^requirement/US (?P<us_joined_inverse_nofirstdots>[\w\-]+)SR: (?P<sysReq>[\w\-]+)/$', views.list_sysReq,
        name='sysReq'),

    url(r'^requirement/Bug Fix- (?P<bugfix>[\w\-]+)/$', views.list_sysReq, name='sysReq'),
    url(r'^requirement/(?P<sysReq>[\w\-]+)/$', views.list_sysReq, name='sysReq'),
    url(r'^requirement/(?P<sysReq>[\w\-]+) / (?P<us_noletters>[\w\-]+)/$', views.list_sysReq, name='sysReq'),
    url(r'^requirement/N/A/$', views.list_sysReq, name='sysReq'),

]