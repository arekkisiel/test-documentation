from django_webtest import WebTest
from django.core.urlresolvers import reverse
from newcat.models import TestGroup, SystemRequirement, Component, TestCase


class TestCaseExportingToXLS(WebTest):
    def setUp(self):
        TestGroup.objects.create(testGroupName='testGroup1').save()
        SystemRequirement.objects.create(sysReq_MKS=123, title='test SR1').save()
        Component.objects.create(componentName='testComponent1').save()
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

    def test_shouldExportWholeGroupToXLS_oneRecord(self):
        testGroupName = TestGroup.objects.get(testGroupName='testGroup1').testGroupName
        response = self.app.get(reverse('export_group', kwargs={'group': testGroupName}))

        self.assertEqual(response.status_code, 200)

    def test_shouldExportWholeSRToXLS_oneRecord(self):
        systemRequirement = SystemRequirement.objects.get(sysReq_MKS=123)
        response = self.app.get(reverse('export_sr', kwargs={'systemRequirement': systemRequirement.sysReq_MKS}))

        self.assertEqual(response.status_code, 200)

    def test_shouldExportWholeComponentToXLS_oneRecord(self):
        componentName = Component.objects.get(componentName='testComponent1').componentName
        response = self.app.get(reverse('export_component', kwargs={'component': componentName}))

        self.assertEqual(response.status_code, 200)

    def test_shouldExportWholeStatusToXLS_oneRecord(self):
        response = self.app.get(reverse('export_status', kwargs={'status': 'Defined'}))

        self.assertEqual(response.status_code, 200)