from django.conf.urls import url

from . import views

urlpatterns = [

    url(r'^testcase/$', views.list_cases, name='list_cases'),
    url(r'^group/(?P<group>[\w\-]+)/$', views.list_group, name='list_group'),
    url(r'^requirement/(?P<systemRequirement>[\w\-]+)/$', views.list_systemRequirement, name='sysReq'),
    url(r'^status/(?P<status>[\w\-]+)/$', views.list_status, name='status'),
    url(r'^component/(?P<component>[\w\-]+)/$', views.list_component, name='component'),
    url(r'^history/$', views.list_changes, name='list_changes'),
    url(r'^testcase/(?P<pk>[0-9]+)/history/$', views.TestCaseHistoryCompareView.as_view(), name='testcase-history' ),

    url(r'^testcase/(?P<testCaseId>[0-9]+)/$', views.test_case, name='test_case'),

    url(r'^testcase/(?P<testCaseId>[0-9]+)/edit/$', views.edit_testcase, name='edit_test_case'),
    url(r'^testcase/(?P<testCaseId>[0-9]+)/edit/steps/$', views.edit_teststeps, name='edit_test_steps'),
    url(r'^testcase/(?P<testCaseId>[0-9]+)/edit/steps/(?P<extraForms>[0-9]+)/$', views.edit_teststeps, name='extra_test_steps'),
    url(r'^testcase/(?P<testCaseId>[0-9]+)/edit/assertions/$', views.edit_expected_results, name='edit_expected_results'),
    url(r'^testcase/(?P<testCaseId>[0-9]+)/edit/assertions/(?P<extraForms>[0-9]+)/$', views.edit_expected_results, name='extra_expected_results'),

    url(r'^create/$', views.create_testcase, name='create_testcase'),
    url(r'^create/save/$', views.create_testcase_late, name='save_testcase'),

    #exports
    url(r'^group/(?P<group>[\w\-]+)/export/$', views.export_list, name='export_group'),
    url(r'^component/(?P<component>[\w\-]+)/export/$', views.export_list, name='export_group'),
    url(r'^requirement/(?P<systemRequirement>[\w\-]+)/export/$', views.export_list, name='export_sr'),
    url(r'^status/(?P<status>[\w\-]+)/export/$', views.export_list, name='export_status'),

    url(r'^error/$', views.error, name='error'),
]