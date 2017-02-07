from django_webtest import WebTest
from django.core.urlresolvers import reverse
from newcat.models import TestGroup, SystemRequirement, Component, TestCaseVersion, TestCase
from newcat.tests.test_forms import getActualTestCaseByTestName


class TestCaseHistoryPresentation(WebTest):
    def setUp(self):
        TestGroup.objects.create(testGroupName='testGroup1', ).save()
        SystemRequirement.objects.create(sysReq_MKS=123, title='test SR1', ).save()
        Component.objects.create(componentName='testComponent1', ).save()
        TestCaseVersion.objects.create(id=1, version=1, comment="testComment", current=True, user="testUser").save()
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
            version=TestCaseVersion.objects.get(id=1)
        ).save()


    def test_shouldTestCaseChangeTriggerVersionUpdate(self):
        testCase = TestCase.objects.get(testName='testName1')
        response = self.app.get(reverse('edit_test_case', kwargs={'testCaseId': testCase.id}))
        edit_testCase_form = response.form
        edit_testCase_form['testName'] = 'testNameEdited'
        edit_testCase_form.submit()
        testCase = TestCase.objects.get(testName='testNameEdited')

        response = self.app.get(reverse('testcase_history', kwargs={'testCaseId': testCase.id}))
        self.assertContains(response, 'testComment')
        self.assertContains(response, 'TestCaseEdited.')
        self.assertContains(response, 'testUser')
        self.assertContains(response, 'default_username2')
        self.assertContains(response, 'False')
        self.assertContains(response, 'True')

    def test_shouldBeAbleToChooseVersionsToCompare(self):
        testCase = TestCase.objects.get(testName='testName1')
        response = self.app.get(reverse('edit_test_case', kwargs={'testCaseId': testCase.id}))
        edit_testCase_form = response.form
        edit_testCase_form['testName'] = 'testNameEdited'
        edit_testCase_form.submit()
        testCase = TestCase.objects.get(testName='testNameEdited')
        response = self.app.get(reverse('testcase_history_compare', kwargs={'testCaseId': testCase.id, 'referenceVersion': 1, 'comparedVersion': 2,}))
        self.assertContains(response, 'testName1')
        self.assertContains(response, 'testNameEdited')

    def test_shouldTestStepsChangeBeVisibleInHistoryView(self):
        testCase = TestCase.objects.get(testName='testName1')
        response = self.app.get(reverse('edit_test_steps', kwargs={'testCaseId': testCase.id}))
        edit_testSteps_form = response.form
        edit_testSteps_form['teststep_set-0-stepOrder'] = 1
        edit_testSteps_form['teststep_set-0-instruction'] = "FirstStep"
        edit_testSteps_form['teststep_set-1-stepOrder'] = 2
        edit_testSteps_form['teststep_set-1-instruction'] = "SecondStep"
        edit_testSteps_form.submit()

        testCase = getActualTestCaseByTestName(self, 'testName1')
        response = self.app.get(reverse('edit_test_steps', kwargs={'testCaseId': testCase.id}))
        edit_testSteps_form = response.form
        edit_testSteps_form['teststep_set-0-delete'] = True
        edit_testSteps_form['teststep_set-1-instruction'] = "SecondStepEdited"
        edit_testSteps_form.submit()

        testCase = getActualTestCaseByTestName(self, 'testName1')
        response = self.app.get(reverse('testcase_history_compare',
                                        kwargs={'testCaseId': testCase.id, 'referenceVersion': 2,
                                                'comparedVersion': 3, }))
        self.assertContains(response, 'FirstStep')
        self.assertContains(response, 'SecondStep')
        self.assertContains(response, 'SecondStepEdited')

    def test_shouldTestStepsCreationBeVisibleInHistoryView(self):
        testCase = TestCase.objects.get(testName='testName1')
        response = self.app.get(reverse('edit_test_steps', kwargs={'testCaseId': testCase.id}))
        edit_testSteps_form = response.form
        edit_testSteps_form['teststep_set-0-stepOrder'] = 1
        edit_testSteps_form['teststep_set-0-instruction'] = "FirstStep"
        edit_testSteps_form['teststep_set-1-stepOrder'] = 2
        edit_testSteps_form['teststep_set-1-instruction'] = "SecondStep"
        edit_testSteps_form.submit()

        testCase = getActualTestCaseByTestName(self, 'testName1')
        response = self.app.get(reverse('testcase_history_compare',
                                        kwargs={'testCaseId': testCase.id, 'referenceVersion': 1,
                                                'comparedVersion': 2, }))
        self.assertContains(response, 'FirstStep')
        self.assertContains(response, 'SecondStep')