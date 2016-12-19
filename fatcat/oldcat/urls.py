from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^/groups/$', views.list_groups, name='list_groups'),
    url(r'^/testcase/$', views.list_cases, name='list_cases'),
    url(r'^/testcase/(?P<testCaseId>[0-9]+)/$', views.test_case, name='test_case'),
]