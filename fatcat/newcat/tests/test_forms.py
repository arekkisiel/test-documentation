from django.contrib.auth.models import User
from django.test import Client
from django.test import TestCase
from django.core.urlresolvers import reverse
from django_webtest import WebTest
from newcat.models import TestCase, Component, TestStep, ExpectedResult, TestGroup, SystemRequirement


def fillInFirstTestCaseForm(self, numberOfCases):
    create_testCase_url = self.app.get(reverse('create_testcase'), user='john')

    create_testCase_form = create_testCase_url.forms['createTestCaseForm']
    create_testCase_form['testCase-testGroup'] = 'testGroup'
    create_testCase_form['testCase-systemRequirement'] = 'MOS-123456'
    create_testCase_form['testCase-component'] = 'testComponent'
    create_testCase_form['testCase-testedFunctionality'] = 'testFunctionality'
    create_testCase_form['testCase-testEngineer'] = 'testEngineer'
    create_testCase_form['testCase-implementedBy'] = 'testImplementedBy'
    create_testCase_form['testCase-numberOfCases'] = numberOfCases

    return create_testCase_form.submit('testCaseSubmit').follow()

class TestCreateOperations(WebTest):
    def setUp(self):
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')

    def test_shouldCreateNewTestGroup(self):
        createTestCase_url = self.app.get(reverse('create_testcase'), user='john')
        createTestGroup_form = createTestCase_url.forms['createNewGroup']

        createTestGroup_form['testGroup-testGroupName'] = 'testGroup'
        createTestGroup_form.submit('testGroupSubmit')

        assert TestGroup.objects.get(testGroupName = 'testGroup') is not None

    def test_shouldCreateNewSystemRequirement(self):
        createTestCase_url = self.app.get(reverse('create_testcase'), user='john')
        createSystemRequirement_form = createTestCase_url.forms['createNewSystemRequirement']

        createSystemRequirement_form['systemRequirement-sysReq_MKS'] = 'MOS-123456'
        createSystemRequirement_form['systemRequirement-title'] = 'testSystemRequirement'
        createSystemRequirement_form.submit('systemRequirementSubmit')

        assert SystemRequirement.objects.get(sysReq_MKS = 'MOS-123456') is not None

    def test_shouldCreateNewComponent(self):
        createTestCase_url = self.app.get(reverse('create_testcase'), user='john')
        createComponent_form = createTestCase_url.forms['createNewComponent']

        createComponent_form['component-componentName'] = 'testComponent'
        createComponent_form.submit('componentSubmit')

        assert Component.objects.get(componentName = 'testComponent') is not None

    def test_shouldCreateOneNewTestCase(self):
        TestGroup.objects.create(testGroupName='testGroup')
        SystemRequirement.objects.create(sysReq_MKS = 'MOS-123456', title = 'testSR')
        Component.objects.create(componentName = 'testComponent')

        create_testCase_lateurl = fillInFirstTestCaseForm(self, 1)

        create_testCase_lateform = create_testCase_lateurl.forms['createTestCaseLateForm']
        create_testCase_lateform['form-0-testName'] = 'testName'
        create_testCase_lateform['form-0-testSituation'] = 'testSituation'
        create_testCase_lateform['form-0-status'] = 'Defined'
        create_testCase_lateform.submit()

        assert TestCase.objects.get(testName='testName') is not None

    def test_shouldCreateTwoNewTestCases(self):
        TestGroup.objects.create(testGroupName='testGroup')
        SystemRequirement.objects.create(sysReq_MKS='MOS-123456', title='testSR')
        Component.objects.create(componentName='testComponent')

        create_testCase_lateurl = fillInFirstTestCaseForm(self, 2)

        create_testCase_lateform = create_testCase_lateurl.forms['createTestCaseLateForm']
        create_testCase_lateform['form-0-testName'] = 'testName1'
        create_testCase_lateform['form-0-testSituation'] = 'testSituation1'
        create_testCase_lateform['form-0-status'] = 'Defined'
        create_testCase_lateform['form-1-testName'] = 'testName2'
        create_testCase_lateform['form-1-testSituation'] = 'testSituation2'
        create_testCase_lateform['form-1-status'] = 'Implemented'
        create_testCase_lateform.submit()

        assert TestCase.objects.get(testName='testName1') is not None
        assert TestCase.objects.get(testName='testName2') is not None

    def test_shouldCreateNewTestCaseWithEmptyCases(self):
        TestGroup.objects.create(testGroupName='testGroup')
        SystemRequirement.objects.create(sysReq_MKS='MOS-123456', title='testSR')
        Component.objects.create(componentName='testComponent')


        create_testCase_lateurl = fillInFirstTestCaseForm(self, 2)

        create_testCase_lateform = create_testCase_lateurl.forms['createTestCaseLateForm']
        create_testCase_lateform['form-0-testName'] = 'testName1'
        create_testCase_lateform['form-0-testSituation'] = 'testSituation1'
        create_testCase_lateform['form-0-status'] = 'Defined'
        create_testCase_lateform.submit()

        assert TestCase.objects.get(testName='testName1') is not None




class TestEditOperations(WebTest):

    def setUp(self):
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        TestGroup.objects.create(testGroupName='testGroup1',).save()
        TestGroup.objects.create(testGroupName='testGroup2', ).save()
        SystemRequirement.objects.create(sysReq_MKS=123, title='test SR1',).save()
        SystemRequirement.objects.create(sysReq_MKS=321, title='test SR2', ).save()
        Component.objects.create(componentName='testComponent1', ).save()
        Component.objects.create(componentName='testComponent2', ).save()

        TestCase.objects.create(
            testName='testName',
            testedFunctionality ='testFunctionality',
            testEngineer='testEngineer',
            implementedBy='testImplementedBy',
            testSituation='testSituation',
            status='Defined',
            testGroup=TestGroup.objects.get(testGroupName='testGroup1'),
            systemRequirement=SystemRequirement.objects.get(sysReq_MKS=123),
            component=Component.objects.get(componentName = 'testComponent1'),
        ).save()

    def test_shouldEditWholeTestCase(self):
        testCase = TestCase.objects.get(testName='testName')
        editGroup = TestGroup.objects.get(testGroupName='testGroup2')
        editSystemRequirement = SystemRequirement.objects.get(sysReq_MKS = 321)
        editComponent = Component.objects.get(componentName = 'testComponent2')
        response = self.app.get(reverse('edit_test_case', kwargs={'testCaseId': testCase.id}), user='john')

        edit_testCase_form = response.form
        edit_testCase_form['testName'] = 'testNameEdited'
        edit_testCase_form['testGroup'] = editGroup
        edit_testCase_form['systemRequirement'] = 321
        edit_testCase_form['component'] = editComponent
        edit_testCase_form['testedFunctionality'] = 'testFunctionalityEdited'
        edit_testCase_form['testEngineer'] = 'testEngineerEdited'
        edit_testCase_form['implementedBy'] = 'testImplementedByEdited'
        edit_testCase_form['testSituation'] = 'testSituationEdited'
        edit_testCase_form['status'] = 'Implemented'
        edit_testCase_form.submit()
        testCaseEdited = TestCase.objects.get(testName='testNameEdited')

        assert testCaseEdited is not None
        self.assertEqual(testCaseEdited.testName, 'testNameEdited')
        self.assertEqual(testCaseEdited.testGroup, editGroup)
        self.assertEqual(testCaseEdited.systemRequirement, editSystemRequirement)
        self.assertEqual(testCaseEdited.component, editComponent)
        self.assertEqual(testCaseEdited.testedFunctionality, 'testFunctionalityEdited')
        self.assertEqual(testCaseEdited.testEngineer, 'testEngineerEdited')
        self.assertEqual(testCaseEdited.implementedBy, 'testImplementedByEdited')
        self.assertEqual(testCaseEdited.testSituation, 'testSituationEdited')
        self.assertEqual(testCaseEdited.status, 'Implemented')

    def test_shouldEditPartOfTestCase(self):
        testCase = TestCase.objects.get(testName='testName')
        editGroup = TestGroup.objects.get(testGroupName='testGroup2')
        editComponent = Component.objects.get(componentName = 'testComponent2')

        response = self.app.get(reverse('edit_test_case', kwargs={'testCaseId': testCase.id}), user='john')

        edit_testCase_form = response.form
        edit_testCase_form['testName'] = 'testNameEdited'
        edit_testCase_form['testGroup'] = editGroup
        edit_testCase_form['component'] = editComponent
        edit_testCase_form['testedFunctionality'] = 'testFunctionalityEdited'
        edit_testCase_form['implementedBy'] = 'testImplementedByEdited'
        edit_testCase_form['testSituation'] = 'testSituationEdited'
        edit_testCase_form.submit()
        testCaseEdited = TestCase.objects.get(testName='testNameEdited')

        assert testCaseEdited is not None
        self.assertEqual(testCaseEdited.testName, 'testNameEdited')
        self.assertEqual(testCaseEdited.testGroup, editGroup)
        self.assertEqual(testCaseEdited.systemRequirement, SystemRequirement.objects.get(sysReq_MKS = 123))
        self.assertEqual(testCaseEdited.component, editComponent)
        self.assertEqual(testCaseEdited.testedFunctionality, 'testFunctionalityEdited')
        self.assertEqual(testCaseEdited.testEngineer, 'testEngineer')
        self.assertEqual(testCaseEdited.implementedBy, 'testImplementedByEdited')
        self.assertEqual(testCaseEdited.testSituation, 'testSituationEdited')
        self.assertEqual(testCaseEdited.status, 'Defined')

    def test_shouldDefineTestSteps(self):
        testCase = TestCase.objects.get(testName='testName', current=True)
        response = self.app.get(reverse('edit_test_steps', kwargs={'testCaseId': testCase.id}), user='john')
        edit_testSteps_form = response.form
        edit_testSteps_form['form-0-stepOrder'] = 1
        edit_testSteps_form['form-0-instruction'] = "FirstStep"
        edit_testSteps_form['form-1-stepOrder'] = 2
        edit_testSteps_form['form-1-instruction'] = "SecondStep"
        edit_testSteps_form['form-2-stepOrder'] = 3
        edit_testSteps_form['form-2-instruction'] = "ThirdStep"
        edit_testSteps_form.submit()

        testCase = TestCase.objects.get(testName='testName', current=True)

        testStepsQueryset = TestStep.objects.filter(testCaseUUID = testCase.testCaseUUID, current=True)
        self.assertQuerysetEqual(testStepsQueryset, ['<TestStep: FirstStep>', '<TestStep: SecondStep>', '<TestStep: ThirdStep>'])

    def test_shouldUpdateTestSteps(self):
        testCase = TestCase.objects.get(testName='testName')
        response = self.app.get(reverse('edit_test_steps', kwargs={'testCaseId': testCase.id}), user='john')
        edit_testSteps_form = response.form
        edit_testSteps_form['form-0-stepOrder'] = 1
        edit_testSteps_form['form-0-instruction'] = "FirstStep"
        edit_testSteps_form['form-1-stepOrder'] = 2
        edit_testSteps_form['form-1-instruction'] = "SecondStep"
        edit_testSteps_form['form-2-stepOrder'] = 3
        edit_testSteps_form['form-2-instruction'] = "ThirdStep"
        edit_testSteps_form.submit()

        testCase = TestCase.objects.get(testName='testName', current=True)

        response = self.app.get(reverse('edit_test_steps', kwargs={'testCaseId': testCase.id}), user='john')
        edit_testSteps_form = response.form
        edit_testSteps_form['form-0-delete'] = True
        edit_testSteps_form['form-1-instruction'] = "SecondStepEdited"
        edit_testSteps_form.submit()

        testCase = TestCase.objects.get(testName='testName', current=True)

        testStepsQueryset = TestStep.objects.filter(testCaseUUID = testCase.testCaseUUID, current=True)
        self.assertQuerysetEqual(testStepsQueryset, ['<TestStep: SecondStepEdited>', '<TestStep: ThirdStep>'])

    def test_shouldDefineTestAsserts(self):
        testCase = TestCase.objects.get(testName='testName')
        response = self.app.get(reverse('edit_expected_results', kwargs={'testCaseId': testCase.id}), user='john')
        edit_testAssertions_form = response.form
        edit_testAssertions_form['form-0-assertType'] = "TRUE"
        edit_testAssertions_form['form-0-expectedResult'] = "FirstAssert"
        edit_testAssertions_form['form-1-assertType'] = "NOT EQUALS"
        edit_testAssertions_form['form-1-expectedResult'] = "SecondAssert"
        edit_testAssertions_form['form-2-assertType'] = "THAT"
        edit_testAssertions_form['form-2-expectedResult'] = "ThirdAssert"
        edit_testAssertions_form.submit()

        testAssertionsQueryset = ExpectedResult.objects.filter(testCaseUUID=testCase.testCaseUUID, current=True)
        self.assertQuerysetEqual(testAssertionsQueryset.order_by('assertType'),
                                 ['<ExpectedResult: SecondAssert>', '<ExpectedResult: ThirdAssert>', '<ExpectedResult: FirstAssert>'])

    def test_shouldUpdateTestAsserts(self):
        testCase = TestCase.objects.get(testName='testName')
        response = self.app.get(reverse('edit_expected_results', kwargs={'testCaseId': testCase.id}), user='john')
        edit_testAssertions_form = response.form
        edit_testAssertions_form['form-0-assertType'] = "TRUE"
        edit_testAssertions_form['form-0-expectedResult'] = "FirstAssert"
        edit_testAssertions_form['form-1-assertType'] = "NOT EQUALS"
        edit_testAssertions_form['form-1-expectedResult'] = "SecondAssert"
        edit_testAssertions_form['form-2-assertType'] = "THAT"
        edit_testAssertions_form['form-2-expectedResult'] = "ThirdAssert"
        edit_testAssertions_form.submit()

        testCase = TestCase.objects.get(testName='testName')
        response = self.app.get(reverse('edit_expected_results', kwargs={'testCaseId': testCase.id}), user='john')
        edit_testAssertions_form = response.form
        edit_testAssertions_form['form-0-assertType'] = "CONTAINS"
        edit_testAssertions_form['form-0-expectedResult'] = "FirstAssertEdited"
        edit_testAssertions_form['form-2-delete'] = True
        edit_testAssertions_form.submit()

        testAssertionsQueryset = ExpectedResult.objects.filter(testCaseUUID=testCase.testCaseUUID, current=True)
        self.assertQuerysetEqual(testAssertionsQueryset.order_by('assertType'),
                                 ['<ExpectedResult: FirstAssertEdited>', '<ExpectedResult: SecondAssert>'])

    def test_shouldTestCaseUpdateNotDeleteTestSteps(self):
        testCase = TestCase.objects.get(testName='testName')
        response = self.app.get(reverse('edit_test_steps', kwargs={'testCaseId': testCase.id}), user='john')
        edit_testSteps_form = response.form
        edit_testSteps_form['form-0-stepOrder'] = 1
        edit_testSteps_form['form-0-instruction'] = "FirstStep"
        edit_testSteps_form['form-1-stepOrder'] = 2
        edit_testSteps_form['form-1-instruction'] = "SecondStep"
        edit_testSteps_form.submit()

        testCase = TestCase.objects.get(testName='testName', current=True)
        response = self.app.get(reverse('edit_test_case', kwargs={'testCaseId': testCase.id}), user='john')
        edit_testCase_form = response.form
        edit_testCase_form['testName'] = 'testNameEdited'
        edit_testCase_form.submit()
        testCase = TestCase.objects.get(testName='testNameEdited', current=True)
        response = self.app.get(reverse('test_case', kwargs={'testCaseId': testCase.id}))

        self.assertContains(response, 'testNameEdited')
        self.assertContains(response, 'testEngineer')
        self.assertContains(response, 'FirstStep')
        self.assertContains(response, 'SecondStep')
