from django.forms import formset_factory, inlineformset_factory
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template import RequestContext
from django.template import loader
from django.template.response import TemplateResponse
from django.shortcuts import get_object_or_404
from .models import TestCase, TestStep, TestGroup, ExpectedResult, TestCaseForm, TestStepsForm, ExpectedResultForm, \
    TestGroupForm, RequirementForm, SystemRequirement


#### List Views

def list_sysReq(request, sysReq):
    testCasesList = TestCase.objects.filter(systemRequirement = sysReq)
    context = RequestContext(request, {'testCasesList': testCasesList})
    return TemplateResponse(request, 'newcat/list_cases.html', context)

def list_status(request, status):
    testCasesList = TestCase.objects.filter(status = status)
    context = RequestContext(request, {'testCasesList': testCasesList})
    return TemplateResponse(request, 'newcat/list_cases.html', context)

def list_cases(request):
    testCasesList = TestCase.objects.all()
    context = RequestContext(request, {'testCasesList': testCasesList})
    return TemplateResponse(request, 'newcat/list_cases.html', context)

def test_case(request, testCaseId):
    testCase = TestCase.objects.get(id=testCaseId)
    testStepsList = TestStep.objects.filter(testCase = testCase.id)
    testStepsList = testStepsList.order_by('stepOrder')
    expectedResultsList = ExpectedResult.objects.filter(testCase=testCase)
    context = {'testCase': testCase,
               'testStepsList': testStepsList,
               'expectedResultsList': expectedResultsList}
    return render(request, 'newcat/testcase.html', context)

#### Create Views

def create_testcase(request):
    testCaseForm = TestCaseForm()
    testStepsFormset = formset_factory(TestStepsForm, extra=3)
    expectedResultFormset = formset_factory(ExpectedResultForm, extra=3)
    if request.method == 'POST':
        testCaseForm = TestCaseForm(request.POST)
        testStepsFormset = testStepsFormset(request.POST, request.FILES)
        expectedResultFormset = expectedResultFormset(request.POST, request.FILES)
        testGroup = testCaseForm.data['testGroup']
        systemRequirement = testCaseForm.data['systemRequirement']

        new_testcase = TestCase(
            testName = testCaseForm.data['testName'],
            testGroup = TestGroup.objects.get(testGroupName = testGroup),
            systemRequirement=SystemRequirement.objects.get(sysReq_MKS = systemRequirement),
            testedFunctionality = testCaseForm.data['testedFunctionality'],
            testEngineer = testCaseForm.data['testEngineer'],
            implementedBy = testCaseForm.data['implementedBy'],
            testSituation = testCaseForm.data['testSituation'],
            status = testCaseForm.data['status'])
        new_testcase.save()

        for form in testStepsFormset:
            if form.is_valid():
                testStepData = form.cleaned_data
                if testStepData:
                    new_teststep = TestStep(
                        testCase = new_testcase,
                        instruction = testStepData['instruction'],
                        stepOrder = testStepData['stepOrder']
                    )
                    new_teststep.save()
        for form in expectedResultFormset:
            if form.is_valid():
                expectedResultData = form.cleaned_data
                if expectedResultData:
                    new_expectedResult = ExpectedResult(
                        assertType = expectedResultData['assertType'],
                        expectedResult = expectedResultData['expectedResult'],
                        testCase = new_testcase
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
    return render(request, 'newcat/testcase_create.html', context)

def create_testgroup(request):
    form = TestGroupForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            new_testgroup = TestGroup(testGroupName = form.data['testGroupName'])
            new_testgroup.save()
            return HttpResponseRedirect("/newcat/close/")
    template = loader.get_template('newcat/testgroup_create.html')
    context = RequestContext(request, {
        'form': form,
    })
    return HttpResponse(template.render(context))

def create_requirement(request):
    form = RequirementForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            new_requirement = SystemRequirement(sysReq_MKS = form.data['sysReq_MKS'], title = form.data['title'])
            new_requirement.save()
            return HttpResponseRedirect("/newcat/close/")
    template = loader.get_template('newcat/requirement_create.html')
    context = RequestContext(request, {
        'form': form,
    })
    return HttpResponse(template.render(context))

#### Edit and Delete Views

def edit_testcase(request, testCaseId):
    testCaseInstance = get_object_or_404(TestCase, id=testCaseId)
    testCaseForm = TestCaseForm(request.POST or None, instance=testCaseInstance)
    if request.method == 'POST':
        testCaseForm.save()
        return HttpResponseRedirect('/newcat/testcase/'+testCaseId)
    else:
        context = RequestContext(request, {
            'testCaseInstance': testCaseInstance,
            'testCaseForm': testCaseForm
    })
    return render(request, 'newcat/testcase_update.html', context)

def edit_teststeps(request, testCaseId):
    testStepsFormset = inlineformset_factory(TestCase, TestStep, form=TestStepsForm, extra=3)
    if request.method == 'POST':
        formset = testStepsFormset(request.POST or None, instance=TestCase.objects.get(id=testCaseId))
        if formset.is_valid():
            formset.save()
        return HttpResponseRedirect('/newcat/testcase/'+testCaseId)
    else:
        formset = testStepsFormset(instance=TestCase.objects.get(id=testCaseId))
        context = RequestContext(request, {
            'testCaseId': testCaseId,
            'formset': formset
    })
    return render(request, 'newcat/teststeps_update.html', context)

def edit_expected_results(request, testCaseId):
    expectedResultsFormset = inlineformset_factory(TestCase, ExpectedResult, form=ExpectedResultForm, extra=3)
    if request.method == 'POST':
        formset = expectedResultsFormset(request.POST or None, instance=TestCase.objects.get(id=testCaseId))
        if formset.is_valid():
            formset.save()
        return HttpResponseRedirect('/newcat/testcase/'+testCaseId)
    else:
        formset = expectedResultsFormset(instance=TestCase.objects.get(id=testCaseId))
        context = RequestContext(request, {
            'testCaseId': testCaseId,
            'formset': formset
    })
    return render(request, 'newcat/expectedresults_update.html', context)

#### Universal Views

def index(request):
    return render(request, 'newcat/index.html')

def close_window(request):
    return render(request, 'newcat/close.html')
