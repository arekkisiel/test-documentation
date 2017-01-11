from django.db import models

# Create your models here.
from django import forms


class TestGroup(models.Model):
    testGroupName = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.testGroupName

class Component(models.Model):
    componentName = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.componentName

class SystemRequirement(models.Model):
    sysReq_MKS = models.BigIntegerField(unique=True)
    title = models.CharField(max_length=100, unique=True)

    def __int__(self):
        return self.sysReq_MKS
    def __str__(self):
        return repr(self.sysReq_MKS)+ "  " + self.title


class TestCase(models.Model):
    testName = models.CharField(max_length=200)
    testedFunctionality = models.CharField(max_length=200)
    testEngineer = models.CharField(max_length=200)
    implementedBy = models.CharField(max_length=200)
    testSituation = models.CharField(max_length=1000)
    testGroup = models.ForeignKey(TestGroup, to_field='testGroupName')
    systemRequirement = models.ForeignKey(SystemRequirement, to_field='sysReq_MKS')
    component = models.ForeignKey(Component, to_field='componentName')
    DEFINED = 'Defined'
    IMPLEMENTED = 'Implemented'
    OPERATIONAL = 'Operational'
    IGNORED = 'Ignored'
    DELETED = 'Deleted'
    STATUS= (
		(DEFINED, 'Defined'),
		(IMPLEMENTED, 'Implemented'),
		(OPERATIONAL, 'Operational'),
		(IGNORED, 'Ignored'),
		(DELETED, 'Deleted'),
		)
    status = models.CharField(max_length=11, choices=STATUS)

    def __str__(self):
        return self

class TestStep(models.Model):
    testCase = models.ForeignKey(TestCase, to_field='id', on_delete=models.CASCADE)
    instruction = models.CharField(max_length=1000)
    stepOrder = models.IntegerField()
    class Meta:
        unique_together = ("testCase", "stepOrder")
    def __str__(self):
        return self


class ExpectedResult(models.Model):
    testCase = models.ForeignKey(TestCase, to_field='id', on_delete=models.CASCADE)
    expectedResult = models.CharField(max_length=1000)
    TRUE = 'TRUE'
    FALSE = 'FALSE'
    FAIL = 'FAIL'
    EQUALS = 'EQUALS'
    NOTEQUALS = 'NOT EQUALS'
    CONTAINS = 'CONTAINS'
    NOTNULL = 'NOT NULL'
    THAT = 'THAT'
    CUSTOM = 'CUSTOM'
    ASSERT_TYPE = (
        (TRUE, 'TRUE'),
        (FALSE, 'FALSE'),
        (FAIL, 'FAIL'),
        (EQUALS, 'EQUALS'),
        (NOTEQUALS, 'NOT EQUALS'),
        (CONTAINS, 'CONTAINS'),
        (NOTNULL, 'NOT NULL'),
        (THAT, 'THAT'),
        (CUSTOM, 'CUSTOM')
    )
    assertType = models.CharField(max_length=11, choices=ASSERT_TYPE)

    def __str__(self):
        return self

#### Forms

class TestCaseForm(forms.ModelForm):
    class Meta:
        model = TestCase
        exclude = ()

class TestGroupForm(forms.ModelForm):
    class Meta:
        model = TestGroup
        exclude = ()

class ComponentForm(forms.ModelForm):
    class Meta:
        model = Component
        exclude = ()

class RequirementForm(forms.ModelForm):
    class Meta:
        model = SystemRequirement
        exclude = ()

class ExpectedResultForm(forms.ModelForm):
    class Meta:
        model = ExpectedResult
        exclude = ('testCase',)

class TestStepsForm(forms.ModelForm):
    class Meta:
        model = TestStep
        exclude = ('testCase',)

