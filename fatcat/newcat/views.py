from django.forms import formset_factory
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template import RequestContext
from django.template import loader
from django.template.response import TemplateResponse

from .models import TestCase, TestStep, TestGroup, ExpectedResult, AddTestCase, AddTestGroup, AddExpectedResult, \
    AddTestSteps


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
    testCaseForm = AddTestCase()
    testStepsFormset = formset_factory(AddTestSteps)
    expectedResultFormset = formset_factory(AddExpectedResult)
    if request.method == 'POST':
        testCaseForm = AddTestCase(request.POST)
        testStepsFormset = testStepsFormset(request.POST, request.FILES)
        expectedResultFormset = expectedResultFormset(request.POST, request.FILES)
        testGroup = testCaseForm.data['testGroup']

        new_testcase = TestCase(
            testName = testCaseForm.data['testName'],
            testGroup = TestGroup.objects.get(testGroupName = testGroup),
            testedFunctionality = testCaseForm.data['testedFunctionality'],
            testEngineer = testCaseForm.data['testEngineer'],
            implementedBy = testCaseForm.data['implementedBy'],
            testSituation = testCaseForm.data['testSituation'],
            status = testCaseForm.data['status'])
        new_testcase.save()

        testStepData = testStepsFormset.cleaned_data
        for testStep in testStepsFormset:
            new_teststep = TestStep(
                testCaseId = new_testcase,
                testStep = testStep
            )
            new_teststep.save()

        expectedResultData = expectedResultFormset.cleaned_data
        for expectedResult in expectedResultFormset:
            new_expectedResult = ExpectedResult(
                expectedResult = expectedResult,
                testCaseId = new_testcase
            )
            new_expectedResult.save()
        return HttpResponseRedirect("/newcat/testcase/")
    else:
        testStepsFormset = testStepsFormset()
        expectedResultFormset = expectedResultFormset()
        context = RequestContext(request, {
            'testCaseForm': testCaseForm,
            'testStepsFormset': testStepsFormset,
            'expectedResultFormset': expectedResultFormset,
    })
    return render(request, 'newcat/create_testcase.html', context)

def create_expectedresult(request, testCaseId):
    testCase = TestCase.objects.get(testCaseId = testCaseId)
    expectedResultForm = AddExpectedResult(request.POST)
    if request.method == 'POST':
        formset = expectedResultForm(request.POST, request.FILES, instance=testCase)
        assertType = expectedResultForm.data['assertType']
        expectedResult = expectedResultForm.data['expectedResult']

        new_expectedResult = ExpectedResult(
            assertType = expectedResultForm.data['assertType'],
            expectedResult = expectedResultForm.data['expectedResult'],
            testCaseId = testCaseId
        )
        new_expectedResult.save()
        return HttpResponseRedirect("/newcat/create/")
    else:
        formset = expectedResultForm(instance=testCase)
        return render(request, 'newcat/create_testcase.html', {'formset': formset})

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