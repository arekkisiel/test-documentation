from django.http import HttpResponse
from django.template import RequestContext
from django.template.response import TemplateResponse

from .models import OldCase
from django.shortcuts import render

def list_sysReq(request, sysReq):
    testCasesList = OldCase.objects.filter(system_requirements = sysReq)
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