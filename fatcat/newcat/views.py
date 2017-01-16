from django.forms import inlineformset_factory
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template import RequestContext
from django.template import loader
from django.template.response import TemplateResponse
from django.shortcuts import get_object_or_404
from django.forms.models import modelformset_factory
import xlwt

from .models import TestCase, TestStep, TestGroup, ExpectedResult, TestStepsForm, ExpectedResultForm, \
    TestGroupForm, RequirementForm, SystemRequirement, ComponentForm, Component, TestCaseBaseForm,\
    TestCaseForm


#### List Views

def list_systemRequirement(request, systemRequirement):
    testCasesList = TestCase.objects.filter(systemRequirement = systemRequirement)
    context = RequestContext(request, {'testCasesList': testCasesList, 'systemRequirement': systemRequirement})
    return TemplateResponse(request, 'newcat/list_cases_systemRequirement.html', context)

def list_status(request, status):
    testCasesList = TestCase.objects.filter(status = status)
    context = RequestContext(request, {'testCasesList': testCasesList, 'status': status})
    return TemplateResponse(request, 'newcat/list_cases_status.html', context)

def list_component(request, component):
    testCasesList = TestCase.objects.filter(component = component)
    context = RequestContext(request, {'testCasesList': testCasesList, 'component': component})
    return TemplateResponse(request, 'newcat/list_cases_component.html', context)

def list_group(request, group):
    testCasesList = TestCase.objects.filter(testGroup = group)
    context = RequestContext(request, {'testCasesList': testCasesList, 'group': group})
    return TemplateResponse(request, 'newcat/list_cases_group.html', context)

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
    testCaseForm = TestCaseBaseForm(request.POST or None, prefix='testCase')
    if request.method == 'POST':
        if testCaseForm.is_valid():
            systemRequirement = testCaseForm.data['testCase-systemRequirement']
            testGroup = testCaseForm.data['testCase-testGroup']
            component = testCaseForm.data['testCase-component']
            testedFunctionality = testCaseForm.data['testCase-testedFunctionality']
            testEngineer = testCaseForm.data['testCase-testEngineer']
            implementedBy = testCaseForm.data['testCase-implementedBy']
            request.session['numberOfCases'] = testCaseForm.data['testCase-numberOfCases']
            data = {
                'systemRequirement': systemRequirement,
                'testGroup': testGroup,
                'component': component,
                'testedFunctionality': testedFunctionality,
                'testEngineer': testEngineer,
                'implementedBy': implementedBy}
            request.session['data'] = data
            return HttpResponseRedirect('/newcat/create/save/')
        else:
            return HttpResponseRedirect("/newcat/error/")
    else:
        context = RequestContext(request, {
            'testCaseForm': testCaseForm,
        })
        return render(request, 'newcat/testcase_create.html', context)

def create_testcase_late(request):
    numberOfCases = int(request.session['numberOfCases'])
    dataDict = {}
    for x in range (0, numberOfCases):
        dataDict.update({x: request.session['data']})
    testCaseFormset = modelformset_factory(TestCase, form=TestCaseForm, extra=numberOfCases)
    if request.method == 'POST':
        formset = testCaseFormset(request.POST)
        for form in formset:
            if form.is_valid():
                form.save()
        return HttpResponseRedirect("/newcat/testcase/")
    else:
        queryset = TestCase.objects.none()
        formset = testCaseFormset(queryset=queryset, initial=dataDict)
        context = RequestContext(request, {
            'formset': formset,
            'dataDict': dataDict,
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

#### Exporting to xls

def export_list(request, group=None, component=None, systemRequirement=None, status=None):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Exported.xls"'

    wb = xlwt.Workbook(encoding='utf-8')

    font = xlwt.Font()
    font.bold = True

    pattern = xlwt.Pattern()
    pattern.pattern = xlwt.Pattern.SOLID_PATTERN
    pattern.pattern_fore_colour = xlwt.Style.colour_map['light_orange']

    alignment = xlwt.Alignment()
    alignment.horz = xlwt.Alignment().HORZ_CENTER
    alignment.vert = xlwt.Alignment().VERT_CENTER

    headerStyle = xlwt.XFStyle()
    headerStyle.pattern = pattern
    headerStyle.font = font
    headerStyle.alignment = alignment

    bodyAlignment = xlwt.Alignment()
    bodyAlignment.horz = xlwt.Alignment().HORZ_LEFT

    bodyStyle = xlwt.XFStyle()
    bodyStyle.alignment = bodyAlignment

    generalColumns = ['Id', 'System Requirement', 'Test Group', 'Component', 'Tested Functionality', 'Test Engineer',
                  'ImplementedBy', 'Test Name', 'Test Situation', 'Status']
    specificColumns = ['Step Order', 'Instruction',
               'Assert Type', 'Expected Result']

    # Sheet body, remaining rows
    if group != None:
        testcases = TestCase.objects.filter(testGroup = group).values_list('id', 'systemRequirement', 'testGroup', 'component', 'testedFunctionality', 'testEngineer',
                      'implementedBy', 'testName', 'testSituation', 'status')
    if component != None:
        testcases = TestCase.objects.filter(component = component).values_list('id', 'systemRequirement', 'testGroup', 'component',
                                                                    'testedFunctionality', 'testEngineer',
                                                                    'implementedBy', 'testName', 'testSituation',
                                                                    'status')
    if systemRequirement != None:
        testcases = TestCase.objects.filter(systemRequirement = systemRequirement).values_list('id', 'systemRequirement', 'testGroup',
                                                                             'component',
                                                                             'testedFunctionality', 'testEngineer',
                                                                             'implementedBy', 'testName',
                                                                             'testSituation',
                                                                             'status')

    if status != None:
        testcases = TestCase.objects.filter(status = status).values_list('id', 'systemRequirement', 'testGroup',
                                                                             'component',
                                                                             'testedFunctionality', 'testEngineer',
                                                                             'implementedBy', 'testName',
                                                                             'testSituation',
                                                                             'status')
    for testcase in testcases:
        ws = wb.add_sheet(str(testcase[0]) + '. ' + str(testcase[7]))
        ws.row(0).height_mismatch = True
        ws.row(0).height = 800
        ws.row(2).height_mismatch = True
        ws.row(2).height = 800
        for col_num in range(len(generalColumns)):
            ws.col(col_num).width = 350 * (len(generalColumns[col_num]))
            ws.write(0, col_num, generalColumns[col_num], headerStyle)
        for col_num in range(len(specificColumns)):
            ws.col(col_num).width = 530 * (len(specificColumns[col_num]))
            ws.write(2, col_num, specificColumns[col_num], headerStyle)
        testcase_num = 1
        for col_num in range(len(testcase)):
            ws.write(testcase_num, col_num, testcase[col_num], bodyStyle)
        testSteps = TestStep.objects.filter(testCase = testcase).values_list('stepOrder', 'instruction')
        testAssertions = ExpectedResult.objects.filter(testCase = testcase).values_list('assertType', 'expectedResult')
        teststep_num = testassertion_num =testcase_num
        for teststep in testSteps:
            for col_num in range(len(teststep)):
                ws.write(teststep_num+2, col_num, teststep[col_num], bodyStyle)
            teststep_num += 1
        for testAssertion in testAssertions:
            for col_num in range(len(testAssertion)):
                ws.write(testassertion_num+2, col_num+2, testAssertion[col_num], bodyStyle)
            testassertion_num += 1

    wb.save(response)
    return response

#### Universal Views

def index(request):
    return render(request, 'newcat/index.html')

def close_window(request):
    return render(request, 'newcat/close.html')

def error(request):
    return render(request, 'newcat/error.html')
