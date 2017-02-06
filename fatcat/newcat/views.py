from django.forms import inlineformset_factory
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template import RequestContext
from django.template.response import TemplateResponse
from django.shortcuts import get_object_or_404
from django.forms.models import modelformset_factory
import xlwt

from .models import TestCase, TestStep, TestGroup, ExpectedResult, SystemRequirement,  Component, \
    TestCaseVersion
from .forms import TestStepsForm, ExpectedResultForm, TestGroupForm, ComponentForm, TestCaseBaseForm, TestCaseForm, \
    SystemRequirementForm, TestStepsFormSet


#### List Views

def list_systemRequirement(request, systemRequirement):
    versions = TestCaseVersion.objects.filter(current=True)
    testCasesList = TestCase.objects.filter(systemRequirement=systemRequirement, version = versions)
    context = RequestContext(request, {'testCasesList': testCasesList, 'systemRequirement': systemRequirement})
    return TemplateResponse(request, 'newcat/list_cases_systemRequirement.html', context)


def list_status(request, status):
    versions = TestCaseVersion.objects.filter(current=True)
    testCasesList = TestCase.objects.filter(status=status, version = versions)
    context = RequestContext(request, {'testCasesList': testCasesList, 'status': status})
    return TemplateResponse(request, 'newcat/list_cases_status.html', context)


def list_component(request, component):
    versions = TestCaseVersion.objects.filter(current=True)
    testCasesList = TestCase.objects.filter(component=component, version = versions)
    context = RequestContext(request, {'testCasesList': testCasesList, 'component': component})
    return TemplateResponse(request, 'newcat/list_cases_component.html', context)


def list_group(request, group):
    versions = TestCaseVersion.objects.filter(current=True)
    testCasesList = TestCase.objects.filter(testGroup=group, version = versions)
    context = RequestContext(request, {'testCasesList': testCasesList, 'group': group})
    return TemplateResponse(request, 'newcat/list_cases_group.html', context)


def list_cases(request):
    versions = TestCaseVersion.objects.filter(current=True)
    testCasesList = TestCase.objects.filter(version = versions)
    context = RequestContext(request, {'testCasesList': testCasesList})
    return TemplateResponse(request, 'newcat/list_cases.html', context)


def test_case(request, testCaseId):
    testCase = TestCase.objects.get(id=testCaseId)
    testStepsList = TestStep.objects.filter(testCase=testCase.id)
    testStepsList = testStepsList.order_by('stepOrder')
    expectedResultsList = ExpectedResult.objects.filter(testCase=testCase)
    context = {'testCase': testCase,
               'testStepsList': testStepsList,
               'expectedResultsList': expectedResultsList}
    return render(request, 'newcat/testcase.html', context)


#### Create Views
def create_testcase(request):
    testCaseForm = TestCaseBaseForm(request.POST or None, prefix='testCase')
    testGroupForm = TestGroupForm(request.POST or None, prefix='testGroup')
    systemRequirementForm = SystemRequirementForm(request.POST or None, prefix='systemRequirement')
    componentForm = ComponentForm(request.POST or None, prefix='component')
    if request.method == 'POST':
        if 'componentSubmit' in request.POST:
            if componentForm.is_valid():
                new_component = Component(componentName=componentForm.data['component-componentName'])
                new_component.save()
                context = RequestContext(request, {
                    'testCaseForm': testCaseForm,
                    'testGroupForm': testGroupForm,
                    'systemRequirementForm': systemRequirementForm,
                    'componentForm': componentForm,
                    'newComponent': new_component,
                })
                return render(request, 'newcat/testcase_create.html', context)
        if 'systemRequirementSubmit' in request.POST:
            if systemRequirementForm.is_valid():
                new_requirement = SystemRequirement(
                    sysReq_MKS=systemRequirementForm.data['systemRequirement-sysReq_MKS'],
                    title=systemRequirementForm.data['systemRequirement-title'])
                new_requirement.save()
                context = RequestContext(request, {
                    'testCaseForm': testCaseForm,
                    'testGroupForm': testGroupForm,
                    'systemRequirementForm': systemRequirementForm,
                    'componentForm': componentForm,
                    'newSystemRequirement': new_requirement,
                })
                return render(request, 'newcat/testcase_create.html', context)
        if 'testGroupSubmit' in request.POST:
            if testGroupForm.is_valid():
                new_testgroup = TestGroup(testGroupName=testGroupForm.data['testGroup-testGroupName'])
                new_testgroup.save()
                context = RequestContext(request, {
                    'testCaseForm': testCaseForm,
                    'testGroupForm': testGroupForm,
                    'systemRequirementForm': systemRequirementForm,
                    'componentForm': componentForm,
                    'newTestGroup': new_testgroup,
                })
                return render(request, 'newcat/testcase_create.html', context)
        if 'testCaseSubmit' in request.POST:
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
    context = RequestContext(request, {
        'testCaseForm': testCaseForm,
        'testGroupForm': testGroupForm,
        'systemRequirementForm': systemRequirementForm,
        'componentForm': componentForm,
        'displayErrors': True,
    })
    return render(request, 'newcat/testcase_create.html', context)


def create_testcase_late(request):
    numberOfCases = int(request.session['numberOfCases'])
    dataDict = {}
    for x in range(0, numberOfCases):
        dataDict.update({x: request.session['data']})
    testCaseFormset = modelformset_factory(TestCase, form=TestCaseForm, extra=numberOfCases)
    if request.method == 'POST':
        formset = testCaseFormset(request.POST)
        for form in formset:
            if form.is_valid():
                testCaseVersion = TestCaseVersion(comment = "Test Case Created.", version = 1, user = "default_username")
                testCaseVersion.save()
                testCaseInstance = form.save(commit=False)
                testCaseInstance.version = testCaseVersion
                testCaseInstance.save()
        return HttpResponseRedirect("/newcat/testcase/")
    else:
        queryset = TestCase.objects.none()
        formset = testCaseFormset(queryset=queryset, initial=dataDict)
        context = RequestContext(request, {
            'formset': formset,
            'dataDict': dataDict,
        })
        return render(request, 'newcat/testcase_create_late.html', context)


#### Edit and Delete Views

def edit_testcase(request, testCaseId):
    testCaseInstance = get_object_or_404(TestCase, id=testCaseId)
    if request.method == 'POST':
        testCaseForm = TestCaseForm(request.POST or None)
        if testCaseForm.is_valid():
            newTestCaseInstance = testCaseForm.save(commit=False)
            testCaseVersion = testCaseInstance.version
            testCaseVersion.current = False
            testCaseVersion.save()
            newTestCaseVersion = TestCaseVersion(comment = "TestCaseEdited.", version = testCaseVersion.version + 1, user = "default_username2", testCaseUUID = testCaseVersion.testCaseUUID)
            newTestCaseVersion.save()
            newTestCaseInstance.version = newTestCaseVersion
            newTestCaseInstance.save()
            return HttpResponseRedirect('/newcat/testcase/' + str(newTestCaseInstance.id))
    testCaseForm = TestCaseForm(request.POST or None, instance=testCaseInstance)
    context = RequestContext(request, {
        'testCaseInstance': testCaseInstance,
        'testCaseForm': testCaseForm,
        'displayErrors': True,
    })
    return render(request, 'newcat/testcase_update.html', context)

def edit_teststeps(request, testCaseId, extraForms=3):
    extraForms = int(extraForms)
    testStepsFormset = inlineformset_factory(TestCase, TestStep, form=TestStepsForm, formset=TestStepsFormSet,
                                             extra=extraForms)
    if request.method == 'POST':
        testCase = TestCase.objects.get(id=testCaseId)
        testCaseVersion = testCase.version
        testCaseVersion.current = False
        testCaseVersion.save()
        newTestCaseVersion = TestCaseVersion(comment="TestStepsEdited.", version=testCaseVersion.version + 1,
                                             user="default_username3", testCaseUUID=testCaseVersion.testCaseUUID)
        newTestCaseVersion.save()
        newTestCase = TestCase(testName=testCase.testName, testedFunctionality=testCase.testedFunctionality,
                               testEngineer=testCase.testEngineer, implementedBy=testCase.implementedBy,
                               testSituation=testCase.testSituation, testGroup=testCase.testGroup,
                               systemRequirement=testCase.systemRequirement, component=testCase.component,
                               status=testCase.status, version=newTestCaseVersion)
        newTestCase.version = newTestCaseVersion
        newTestCase.save()
        formset = testStepsFormset(request.POST or None, instance=newTestCase)
        if formset.is_valid():
            formset.save()
            return HttpResponseRedirect('/newcat/testcase/' + str(newTestCase.id))
    formset = testStepsFormset(request.POST or None, instance=TestCase.objects.get(id=testCaseId))
    context = RequestContext(request, {
        'testCaseId': testCaseId,
        'formset': formset,
        'extraForms': extraForms
    })
    return render(request, 'newcat/teststeps_update.html', context)


def edit_expected_results(request, testCaseId, extraForms=3):
    extraForms = int(extraForms)
    expectedResultsFormset = inlineformset_factory(TestCase, ExpectedResult, form=ExpectedResultForm, extra=extraForms)
    if request.method == 'POST':
        formset = expectedResultsFormset(request.POST or None, instance=TestCase.objects.get(id=testCaseId))
        if formset.is_valid():
            formset.save()
            return HttpResponseRedirect('/newcat/testcase/' + testCaseId)
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

    if group != None:
        testcases_list = TestCase.objects.filter(testGroup=group)
        response['Content-Disposition'] = 'attachment; filename="TestGroup"' + group + '".xls"'
    if component != None:
        testcases_list = TestCase.objects.filter(component=component)
        response['Content-Disposition'] = 'attachment; filename="Component"' + component + '".xls"'
    if systemRequirement != None:
        testcases_list = TestCase.objects.filter(systemRequirement=systemRequirement)
        response['Content-Disposition'] = 'attachment; filename="System Requirement"' + systemRequirement + '".xls"'
    if status != None:
        testcases_list = TestCase.objects.filter(status=status)
        response['Content-Disposition'] = 'attachment; filename="Status"' + status + '".xls"'

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
    bodyAlignment.vert = xlwt.Alignment().VERT_CENTER
    bodyAlignment.wrap = 1

    bodyStyle = xlwt.XFStyle()
    bodyStyle.alignment = bodyAlignment

    generalColumns = ['Id', 'System Requirement', 'Test Group', 'Component', 'Tested Functionality', 'Test Engineer',
                      'ImplementedBy', 'Test Name', 'Test Situation', 'Status']
    specificColumns = ['Step Order', 'Instruction',
                       'Assert Type', 'Expected Result']

    testcases = testcases_list.values_list('id', 'systemRequirement', 'testGroup', 'component', 'testedFunctionality',
                                           'testEngineer', 'implementedBy', 'testName', 'testSituation', 'status')
    for testcase in reversed(testcases):
        ws = wb.add_sheet(str(testcase[0]) + '.')
        ws.row(0).height_mismatch = True
        ws.row(0).height = 800
        ws.row(2).height_mismatch = True
        ws.row(2).height = 800
        for col_num in range(len(generalColumns)):
            ws.col(col_num).width = 400 * (len(generalColumns[col_num]))
            ws.write(0, col_num, generalColumns[col_num], headerStyle)
        for col_num in range(len(specificColumns)):
            # Two lines
            # ws.col(col_num).width = 530 * (len(specificColumns[col_num]))
            # ws.write(2, col_num, specificColumns[col_num], headerStyle)
            # One line all
            ws.col(col_num + 10).width = 530 * (len(specificColumns[col_num]))
            ws.write(0, col_num + 10, specificColumns[col_num], headerStyle)
        testcase_num = 1
        for col_num in range(len(testcase)):
            ws.write(testcase_num, col_num, testcase[col_num], bodyStyle)
        testSteps = TestStep.objects.filter(testCase=testcase).values_list('stepOrder', 'instruction')
        testAssertions = ExpectedResult.objects.filter(testCase=testcase).values_list('assertType', 'expectedResult')
        teststep_num = testassertion_num = testcase_num
        for teststep in testSteps:
            for col_num in range(len(teststep)):
                # ws.row(teststep_num+2).height_mismatch = True
                # ws.row(teststep_num+2).height = 800
                # ws.write(teststep_num+2, col_num, teststep[col_num], bodyStyle)
                ws.row(teststep_num).height_mismatch = True
                ws.row(teststep_num).height = 800
                ws.write(teststep_num, col_num + 10, teststep[col_num], bodyStyle)
            teststep_num += 1
        for testAssertion in testAssertions:
            for col_num in range(len(testAssertion)):
                # ws.row(testassertion_num+2).height_mismatch = True
                # ws.row(testassertion_num+2).height = 800
                # ws.write(testassertion_num+2, col_num+2, testAssertion[col_num], bodyStyle)
                ws.row(testassertion_num).height_mismatch = True
                ws.row(testassertion_num).height = 800
                ws.write(testassertion_num, col_num + 12, testAssertion[col_num], bodyStyle)
            testassertion_num += 1

    wb.save(response)
    return response


#### Universal Views

def error(request):
    return render(request, 'newcat/error.html')


####History Views

def list_changes_testcase(request, testCaseId):
    version = TestCase.objects.get(id = testCaseId).version
    versions = TestCaseVersion.objects.filter(testCaseUUID = version.testCaseUUID)
    context = RequestContext(request, {'versions': versions, 'testCaseId': testCaseId})
    return TemplateResponse(request, 'newcat/list_changes.html', context)

def list_changes_testcase_compare(request, testCaseId, referenceVersion, comparedVersion):
    version = TestCase.objects.get(id=testCaseId).version
    referenceVersion = TestCaseVersion.objects.filter(testCaseUUID=version.testCaseUUID, version = referenceVersion)
    comparedVersion = TestCaseVersion.objects.filter(testCaseUUID=version.testCaseUUID, version = comparedVersion)
    referenceTestCase = TestCase.objects.get(version = referenceVersion)
    comparedTestCase = TestCase.objects.get(version = comparedVersion)
    referenceTestSteps = TestStep.objects.filter(testCase = referenceTestCase.id)
    comparetTestSteps = TestStep.objects.filter(testCase = comparedTestCase.id)
    context = RequestContext(request, {'referenceTestCase': referenceTestCase, 'comparedTestCase': comparedTestCase, 'referenceTestSteps': referenceTestSteps, 'comparedTestSteps': comparetTestSteps})
    return TemplateResponse(request, 'newcat/list_changes_compare.html', context)
