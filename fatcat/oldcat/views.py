from django.http import HttpResponse
from django.template import RequestContext
from django.template.response import TemplateResponse

from .models import OldCase
from django.shortcuts import render

def index(request):
    return render(request, 'oldcat/index.html')

def list_groups(request):
    return HttpResponse("Hello, world. You're at the list of test groups.")

def list_cases(request):
    testCasesList = OldCase.objects.all()
    context = RequestContext(request, {'testCasesList': testCasesList})
    return TemplateResponse(request, 'oldcat/list_cases.html', context)

def test_case(request, testCaseId):
    testCase = OldCase.objects.get(id=testCaseId)
    context = {'testCase': testCase}
    return render(request, 'oldcat/test_case.html', context)