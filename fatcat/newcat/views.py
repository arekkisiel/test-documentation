from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template import RequestContext
from django.template import loader
from django.template.response import TemplateResponse

from .models import TestCase, TestStep, TestGroup, ExpectedResult, AddTestCase, AddTestGroup


# Create your views here.
def index(request):
    return render(request, 'newcat/index.html')

def list_sysReq(request, sysReq):
    testCasesList = TestCase.objects.filter(system_requirements = sysReq)
    context = RequestContext(request, {'testCasesList': testCasesList})
    return TemplateResponse(request, 'newcat/list_cases.html', context)

def list_filename(request, filename):
    testCasesList = TestCase.objects.filter(filename = filename + '.csv')
    context = RequestContext(request, {'testCasesList': testCasesList})
    return TemplateResponse(request, 'newcat/list_cases.html', context)

def list_cases(request):
    testCasesList = TestCase.objects.all()
    context = RequestContext(request, {'testCasesList': testCasesList})
    return TemplateResponse(request, 'newcat/list_cases.html', context)

def test_case(request, testCaseId):
    testCase = TestCase.objects.get(id=testCaseId)
    testStepsList = TestStep.objects.filter(testCase = testCase)
    context = {'testCase': testCase,
               'testStepsList': testStepsList}
    return render(request, 'newcat/test_case.html', context)

def create_testcase(request):
    if request.method == 'POST':
        form = AddTestCase(request.POST)
        if form.is_valid():
            testName = form.data['testName']
            testGroup = form.data['testGroup']
            testedFunctionality = form.data['testedFunctionality']
            testEngineer = form.data['testEngineer']
            implementedBy = form.data['implementedBy']
            testSituation = form.data['testSituation']
            expectedResults = form.data['expectedResults']
            status = form.data['status']

            new_testcase = TestCase(
            testName = form.data['testName'],
            testGroup = form.data['testGroup'],
            testedFunctionality = form.data['testedFunctionality'],
            testEngineer = form.data['testEngineer'],
            implementedBy = form.data['implementedBy'],
            testSituation = form.data['testSituation'],
            expectedResults = form.data['expectedResults'],
            status = form.data['status'])
            new_testcase.save()
            return HttpResponseRedirect("/newcat/testcase/")
    else:
        form = AddTestCase()
    template = loader.get_template('newcat/create_testcase.html')
    context = RequestContext(request, {
        'form': form,
    })
    return HttpResponse(template.render(context))

def create_testgroup(request):
    if request.method == 'POST':
        form = AddTestGroup(request.POST)
        if form.is_valid():
            testGroupName = form.data['testGroupName']

            new_testgroup = TestGroup(testGroupName = form.data['testGroupName'])
            new_testgroup.save()
            return HttpResponseRedirect("/newcat/close/")
    else:
        form = AddTestGroup()
    template = loader.get_template('newcat/create_testgroup.html')
    context = RequestContext(request, {
        'form': form,
    })
    return HttpResponse(template.render(context))

def close_window(request):
    return render(request, 'newcat/close.html')