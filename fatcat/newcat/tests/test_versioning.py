from django.contrib.auth.models import User
from django_webtest import WebTest
from django.core.urlresolvers import reverse
from newcat.models import TestGroup, SystemRequirement, Component, TestCase


class TestCaseHistoryPresentation(WebTest):
    def setUp(self):
        User.objects.create_superuser('john', 'lennon@thebeatles.com', 'johnpassword')
        TestGroup.objects.create(testGroupName='testGroup1', ).save()
        SystemRequirement.objects.create(sysReq_MKS=123, title='test SR1', ).save()
        Component.objects.create(componentName='testComponent1', ).save()

        TestCase.objects.create(
            testName='testName1',
            testedFunctionality='testFunctionality1',
            testEngineer='testEngineer1',
            implementedBy='testImplementedBy1',
            testSituation='testSituation1',
            status='Defined',
            testGroup=TestGroup.objects.get(testGroupName='testGroup1'),
            systemRequirement=SystemRequirement.objects.get(sysReq_MKS=123),
            component=Component.objects.get(componentName='testComponent1'),
        ).save()


    def test_shouldTestCaseChangeTriggerVersionUpdate(self):
        testCase = TestCase.objects.get(testName='testName1')
        response = self.app.get(reverse('edit_test_case', kwargs={'testCaseId': testCase.id}), user='john')
        edit_testCase_form = response.form
        edit_testCase_form['testName'] = 'testNameEdited'
        edit_testCase_form.submit()
        testCase = TestCase.objects.get(testName='testNameEdited')

        response = self.app.get(reverse('testcase_history', kwargs={'testCaseId': testCase.id}), user='john')
        self.assertContains(response, '1')
        self.assertContains(response, '2')
        self.assertContains(response, 'False')
        self.assertContains(response, 'True')

    def test_shouldBeAbleToChooseVersionsToCompare(self):
        testCase = TestCase.objects.get(testName='testName1')
        response = self.app.get(reverse('edit_test_case', kwargs={'testCaseId': testCase.id}), user='john')
        edit_testCase_form = response.form
        edit_testCase_form['testName'] = 'testNameEdited'
        edit_testCase_form.submit()
        testCase = TestCase.objects.get(testName='testNameEdited')
        response = self.app.get(reverse('testcase_history_compare', kwargs={'testCaseId': testCase.id, 'referenceVersion': 1, 'comparedVersion': 2,}), user='john')
        self.assertContains(response, 'testName1')
        self.assertContains(response, 'testNameEdited')

    def test_shouldTestStepsChangeBeVisibleInHistoryView(self):
        testCase = TestCase.objects.get(testName='testName1')
        response = self.app.get(reverse('edit_test_steps', kwargs={'testCaseId': testCase.id}), user='john')
        edit_testSteps_form = response.form
        edit_testSteps_form['form-0-stepOrder'] = 1
        edit_testSteps_form['form-0-instruction'] = "FirstStep"
        edit_testSteps_form['form-1-stepOrder'] = 2
        edit_testSteps_form['form-1-instruction'] = "SecondStep"
        edit_testSteps_form.submit()

        response = self.app.get(reverse('edit_test_steps', kwargs={'testCaseId': testCase.id}), user='john')
        edit_testSteps_form = response.form
        edit_testSteps_form['form-0-delete'] = True
        edit_testSteps_form['form-1-instruction'] = "SecondStepEdited"
        edit_testSteps_form.submit()

        testCase = TestCase.objects.get(testName='testName1', current=True)
        response = self.app.get(reverse('teststeps_history_compare',
                                        kwargs={'testCaseId': testCase.id, 'referenceVersion': 1,
                                                'comparedVersion': 2, }), user='john')
        self.assertContains(response, 'FirstStep')
        self.assertContains(response, 'SecondStep')
        self.assertContains(response, 'SecondStepEdited')

    def test_shouldTestStepsCreationBeVisibleInHistoryView(self):
        testCase = TestCase.objects.get(testName='testName1')
        response = self.app.get(reverse('edit_test_steps', kwargs={'testCaseId': testCase.id}), user='john')
        edit_testSteps_form = response.form
        edit_testSteps_form['form-0-stepOrder'] = 1
        edit_testSteps_form['form-0-instruction'] = "FirstStep"
        edit_testSteps_form.submit()
        response = self.app.get(reverse('edit_test_steps', kwargs={'testCaseId': testCase.id}), user='john')
        edit_testSteps_form = response.form
        edit_testSteps_form['form-1-stepOrder'] = 2
        edit_testSteps_form['form-1-instruction'] = "SecondStep"
        edit_testSteps_form.submit()

        response = self.app.get(reverse('teststeps_history_compare',
                                        kwargs={'testCaseId': testCase.id, 'referenceVersion': 1,
                                                'comparedVersion': 2, }), user='john')
        self.assertContains(response, 'FirstStep')
        self.assertContains(response, 'SecondStep')