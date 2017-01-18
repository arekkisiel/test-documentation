from django.http import HttpResponse
from django.template import RequestContext
from django.template.response import TemplateResponse

from .models import OldCase
from django.shortcuts import render

def list_sysReq(request, sysReq=None, us=None, us_nospace=None, us_slashed=None,
                us_dashed=None, us_nospace_inverse=None, bugfix=None, bug=None, us_short=None, us_EMPTY=None,
                us_joined_inverse=None, us_joined_inverse_nofirstdots=None, us_noletters=None, us_short_dotted=None, sr_short=None):
    check = False
    if sysReq:
        if us:
            sysReq = 'SR: ' + sysReq + '\nUS: ' + us
            check = True
        if us_nospace:
            sysReq = 'SR:' + sysReq + '\nUS:' + us_nospace
        if us_slashed:
            sysReq = 'SR: ' + sysReq + ' / US: ' + us_slashed
        if us_dashed:
            sysReq = 'S-R: ' + sysReq + '  \nU-S: ' + us_dashed
        if us_nospace_inverse:
            sysReq = 'US:' + us_nospace_inverse + '\nSR:' + sysReq
        if us_joined_inverse:
            sysReq = 'US: ' + us_joined_inverse + '\nSR: ' + sysReq
        if us_joined_inverse_nofirstdots:
            sysReq = 'US ' + us_joined_inverse_nofirstdots + '\nSR: ' + sysReq
        if us_noletters:
            sysReq = sysReq + ' / ' + us_noletters
    else:
        if sr_short:
            sysReq = 'SR ' + sr_short
        elif us:
            sysReq = 'User Story: ' + us
        elif bugfix:
                sysReq = 'Bug Fix- ' + bugfix
        elif bug:
            sysReq = 'Bug' + bug + 'Test'
        elif us_short:
            sysReq = 'US ' + us_short
        elif us_short_dotted:
            sysReq = 'US: ' + us_short_dotted
        elif us_EMPTY:
            sysReq = 'SR: <EMPTY>\nUS: ' + us_EMPTY
        else:
           sysReq = 'N/A'
    testCasesList = OldCase.objects.filter(system_requirements = sysReq)
    if check:
        if not testCasesList:
            sysReq = sysReq + ' '
            testCasesList = OldCase.objects.filter(system_requirements=sysReq)
    context = RequestContext(request, {'testCasesList': testCasesList})
    return TemplateResponse(request, 'oldcat/list_cases.html', context)

def list_filename(request, filename):
    testCasesList = OldCase.objects.filter(filename = filename + '.csv')
    context = RequestContext(request, {'testCasesList': testCasesList})
    return TemplateResponse(request, 'oldcat/list_cases.html', context)

def list_cases(request):
    testCasesList = OldCase.objects.all()
    context = RequestContext(request, {'testCasesList': testCasesList})
    return TemplateResponse(request, 'oldcat/list_cases.html', context)

def test_case(request, testCaseId):
    testCase = OldCase.objects.get(id=testCaseId)
    context = {'testCase': testCase}
    return render(request, 'oldcat/test_case.html', context)