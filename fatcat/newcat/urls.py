from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.list_cases, name='list_cases'),
    url(r'^testcase/$', views.list_cases, name='list_cases'),
    url(r'^group/(?P<group>[\w\s\-]+)/$', views.list_group, name='list_group'),
    url(r'^requirement/(?P<systemRequirement>[\w\s\-]+)/$', views.list_systemRequirement, name='list_sysReq'),
    url(r'^status/(?P<status>[\w\s]+)/$', views.list_status, name='list_status'),
    url(r'^component/(?P<component>[\w\s\-]+)/$', views.list_component, name='list_component'),


    url(r'^testcase/(?P<testCaseId>[0-9]+)/$', views.test_case, name='test_case'),

    url(r'^testcase/(?P<testCaseId>[0-9]+)/edit/$', views.edit_testcase, name='edit_test_case'),
    url(r'^testcase/(?P<testCaseId>[0-9]+)/edit/steps/$', views.edit_teststeps, name='edit_test_steps'),
    url(r'^testcase/(?P<testCaseId>[0-9]+)/edit/steps/(?P<extraForms>[0-9]+)/$', views.edit_teststeps, name='extra_test_steps'),
    url(r'^testcase/(?P<testCaseId>[0-9]+)/edit/assertions/$', views.edit_expected_results, name='edit_expected_results'),
    url(r'^testcase/(?P<testCaseId>[0-9]+)/edit/assertions/(?P<extraForms>[0-9]+)/$', views.edit_expected_results, name='extra_expected_results'),

    url(r'^create/$', views.create_testcase, name='create_testcase'),
    url(r'^create/save/$', views.create_testcase_late, name='save_testcase'),

    #exports
    url(r'^group/(?P<group>[\w\s\-]+)/export/$', views.export_list, name='export_group'),
    url(r'^component/(?P<component>[\w\s\-]+)/export/$', views.export_list, name='export_component'),
    url(r'^requirement/(?P<systemRequirement>[\w\s\-]+)/export/$', views.export_list, name='export_sr'),
    url(r'^status/(?P<status>[\w\s\-]+)/export/$', views.export_list, name='export_status'),

    url(r'^error/$', views.error, name='error'),

    url(r'^testcase/(?P<testCaseId>[0-9]+)/history/$', views.list_changes_testcase, name='testcase_history' ),
    url(r'^testcase/(?P<testCaseId>[0-9]+)/history/compare/testcase/(?P<referenceVersion>[0-9]+)/(?P<comparedVersion>[0-9]+)/$',
        views.list_changes_testcase_compare, name='testcase_history_compare' ),
    url(r'^testcase/(?P<testCaseId>[0-9]+)/history/compare/teststeps/(?P<referenceVersion>[0-9]+)/(?P<comparedVersion>[0-9]+)/$',
        views.list_changes_teststeps_compare, name='teststeps_history_compare'),
    url(r'^testcase/(?P<testCaseId>[0-9]+)/history/compare/assertions/(?P<referenceVersion>[0-9]+)/(?P<comparedVersion>[0-9]+)/$',
        views.list_changes_assertions_compare, name='assertions_history_compare'),
]