from django.test import TestCase
from django.core.urlresolvers import reverse
from django_webtest import WebTest
from newcat.models import TestCase, Component, TestCaseHistory
from newcat.models import TestGroup
from newcat.models import SystemRequirement

class TestDataPresentation(WebTest):
    def setUp(self):
        TestGroup.objects.create(testGroupName='testGroup1', ).save()
        TestGroup.objects.create(testGroupName='testGroup2', ).save()
        SystemRequirement.objects.create(sysReq_MKS=123, title='test SR1', ).save()
        SystemRequirement.objects.create(sysReq_MKS=321, title='test SR2', ).save()
        Component.objects.create(componentName='testComponent1', ).save()
        TestCaseHistory.objects.create(id=1).save()
        TestCaseHistory.objects.create(id=2).save()
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
            history=TestCaseHistory.objects.get(id=1),
        ).save()
        TestCase.objects.create(
            testName='testName2',
            testedFunctionality='testFunctionality2',
            testEngineer='testEngineer2',
            implementedBy='testImplementedBy2',
            testSituation='testSituation2',
            status='Deleted',
            testGroup=TestGroup.objects.get(testGroupName='testGroup2'),
            systemRequirement=SystemRequirement.objects.get(sysReq_MKS=321),
            component=Component.objects.get(componentName='testComponent1'),
            history=TestCaseHistory.objects.get(id=2),
        ).save()

    def test_listCasesShouldShowAllTestCases(self):
        response = self.app.get(reverse('list_cases'))

        self.assertContains(response, 'testName1')
        self.assertContains(response, 'testName2')

    def test_listStatusShouldShowCorrectTestCases(self):
        response1 = self.app.get(reverse('list_status', kwargs={'status': 'Defined'}))
        response2 = self.app.get(reverse('list_status', kwargs={'status': 'Implemented'}))
        response3 = self.app.get(reverse('list_status', kwargs={'status': 'Deleted'}))

        self.assertContains(response1, 'testName1')
        self.assertNotContains(response2, 'testName1')
        self.assertNotContains(response2, 'testName2')
        self.assertContains(response3, 'testName2')

    def test_listComponentShouldShowCorrectTestCases(self):
        response1 = self.app.get(reverse('list_component', kwargs={'component': Component.objects.get(componentName='testComponent1')}))

        self.assertContains(response1, 'testName1')
        self.assertContains(response1, 'testName2')

    def test_listGroupShouldShowCorrectTestCases(self):
        response1 = self.app.get(reverse('list_group', kwargs={'group': TestGroup.objects.get(testGroupName='testGroup1')}))
        response2 = self.app.get(reverse('list_group', kwargs={'group': TestGroup.objects.get(testGroupName='testGroup2')}))

        self.assertContains(response1, 'testName1')
        self.assertNotContains(response1, 'testName2')
        self.assertContains(response2, 'testName2')
        self.assertNotContains(response2, 'testName1')

    def test_listSystemRequirementShouldShowCorrectTestCases(self):
        response1 = self.app.get(reverse('list_sysReq', kwargs={'systemRequirement': 123}))
        response2 = self.app.get(reverse('list_sysReq', kwargs={'systemRequirement': 321}))

        self.assertContains(response1, 'testName1')
        self.assertNotContains(response1, 'testName2')
        self.assertContains(response2, 'testName2')
        self.assertNotContains(response2, 'testName1')

    def test_testCaseViewShouldShowAllDetails(self):
        testCaseId = TestCase.objects.get(testName = 'testName1').id
        response = self.app.get(reverse('test_case', kwargs={'testCaseId': testCaseId}))

        self.assertContains(response, testCaseId)
        self.assertContains(response, 'testName1')
        self.assertContains(response, 'testGroup1')
        self.assertContains(response, '123')
        self.assertContains(response, 'testFunctionality1')
        self.assertContains(response, 'testEngineer1')
        self.assertContains(response, 'testImplementedBy1')
        self.assertContains(response, 'Defined')
        self.assertContains(response, 'testSituation1')