from django.core.urlresolvers import reverse
from django.forms import formset_factory, inlineformset_factory
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template import RequestContext
from django.template import loader
from django.template.response import TemplateResponse
from django.shortcuts import get_object_or_404
from .models import TestCase, TestStep, TestGroup, ExpectedResult, TestStepsForm, ExpectedResultForm, \
    TestGroupForm, RequirementForm, SystemRequirement, ComponentForm, Component, TestCaseBaseForm, TestCaseLateForm, \
    TestCaseForm


#### List Views

def list_sysReq(request, sysReq):
    testCasesList = TestCase.objects.filter(systemRequirement = sysReq)
    context = RequestContext(request, {'testCasesList': testCasesList})
    return TemplateResponse(request, 'newcat/list_cases.html', context)

def list_status(request, status):
    testCasesList = TestCase.objects.filter(status = status)
    context = RequestContext(request, {'testCasesList': testCasesList})
    return TemplateResponse(request, 'newcat/list_cases.html', context)

def list_component(request, component):
    testCasesList = TestCase.objects.filter(component = component)
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

def create_testcase_base(request):
    testCaseForm = TestCaseBaseForm(request.POST or None)
    if request.method == 'POST':
        if testCaseForm.is_valid():
            request.session['sr'] = testCaseForm.data['systemRequirement']
            request.session['testGroup'] = testCaseForm.data['testGroup']
            request.session['component'] = testCaseForm.data['component']
            request.session['testedFunctionality'] = testCaseForm.data['testedFunctionality']
            request.session['testEngineer'] = testCaseForm.data['testEngineer']
            request.session['implementedBy'] = testCaseForm.data['implementedBy']
            return HttpResponseRedirect('cases')
        else:
            return HttpResponseRedirect("/newcat/error/")
    else:
        context = RequestContext(request, {
            'testCaseForm': testCaseForm,
        })
        return render(request, 'newcat/testcase_create.html', context)

def create_testcase_late(request):
    testCaseLateForm = TestCaseLateForm(request.POST or None)
    if request.method == 'POST':
        if testCaseLateForm.is_valid():
            new_testcase = TestCase(
                systemRequirement = SystemRequirement.objects.get(sysReq_MKS = request.session['sr']),
                component = Component.objects.get(componentName=request.session['component']),
                testedFunctionality = request.session['testedFunctionality'],
                testEngineer = request.session['testEngineer'],
                implementedBy = request.session['implementedBy'],
                testName = testCaseLateForm.data['testName'],
                testGroup = TestGroup.objects.get(testGroupName=request.session['testGroup']),
                testSituation=testCaseLateForm.data['testSituation'],
                status=testCaseLateForm.data['status']
            )
            new_testcase.save()
            return HttpResponseRedirect("/newcat/testcase/")
        else:
            return HttpResponseRedirect("/newcat/error/")
    else:
        context = RequestContext(request, {
            'testCaseLateForm': testCaseLateForm,
        })
        return render(request, 'newcat/testcase_create_late.html', context)



def create_testgroup(request):
    form = TestGroupForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            new_testgroup = TestGroup(testGroupName = form.data['testGroupName'])
            new_testgroup.save()
            return HttpResponseRedirect("/newcat/close/")
        else:
            return HttpResponseRedirect("/newcat/error/")
    template = loader.get_template('newcat/testgroup_create.html')
    context = RequestContext(request, {
        'form': form,
    })
    return HttpResponse(template.render(context))

def create_component(request):
    form = ComponentForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            new_component = Component(componentName = form.data['componentName'])
            new_component.save()
            return HttpResponseRedirect("/newcat/close/")
        else:
            return HttpResponseRedirect("/newcat/error/")
    template = loader.get_template('newcat/component_create.html')
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
        else:
            return HttpResponseRedirect("/newcat/error/")
    template = loader.get_template('newcat/requirement_create.html')
    context = RequestContext(request, {
        'form': form,
    })
    return HttpResponse(template.render(context))

#### Edit and Delete Views

def edit_testcase(request, testCaseId):
    testCaseInstance = get_object_or_404(TestCase, id=testCaseId)
    if request.method == 'POST':
        testCaseForm = TestCaseForm(request.POST or None, instance=testCaseInstance)
        if testCaseForm.is_valid():
            testCaseForm.save()
            return HttpResponseRedirect('/newcat/testcase/'+testCaseId)
        else:
            return HttpResponseRedirect("/newcat/error/")
    else:
        testCaseForm = TestCaseForm(instance=testCaseInstance)
        context = RequestContext(request, {
            'testCaseInstance': testCaseInstance,
            'testCaseForm': testCaseForm
    })
    return render(request, 'newcat/testcase_update.html', context)

def edit_teststeps(request, testCaseId, extraForms=3):
    extraForms = int(extraForms)
    testStepsFormset = inlineformset_factory(TestCase, TestStep, form=TestStepsForm, extra=extraForms)
    if request.method == 'POST':
        formset = testStepsFormset(request.POST or None, instance=TestCase.objects.get(id=testCaseId))
        if formset.is_valid():
            formset.save()
            return HttpResponseRedirect('/newcat/testcase/'+testCaseId)
        else:
            return HttpResponseRedirect("/newcat/error/")
    else:
        formset = testStepsFormset(instance=TestCase.objects.get(id=testCaseId))
        context = RequestContext(request, {
            'testCaseId': testCaseId,
            'formset': formset,
            'extraForms': extraForms,
    })
    return render(request, 'newcat/teststeps_update.html', context)

def edit_expected_results(request, testCaseId, extraForms=3):
    extraForms=int(extraForms)
    expectedResultsFormset = inlineformset_factory(TestCase, ExpectedResult, form=ExpectedResultForm, extra=extraForms)
    if request.method == 'POST':
        formset = expectedResultsFormset(request.POST or None, instance=TestCase.objects.get(id=testCaseId))
        if formset.is_valid():
            formset.save()
            return HttpResponseRedirect('/newcat/testcase/'+testCaseId)
        else:
            return HttpResponseRedirect("/newcat/error/")
    else:
        formset = expectedResultsFormset(instance=TestCase.objects.get(id=testCaseId))
        context = RequestContext(request, {
            'testCaseId': testCaseId,
            'formset': formset,
            'extraForms': extraForms,
    })
    return render(request, 'newcat/expectedresults_update.html', context)

#### Universal Views

def index(request):
    return render(request, 'newcat/index.html')

def close_window(request):
    return render(request, 'newcat/close.html')

def error(request):
    return render(request, 'newcat/error.html')
