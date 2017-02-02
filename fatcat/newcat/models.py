from django.db import models
import reversion
from django.forms import BaseInlineFormSet
from reversion_compare.views import HistoryCompareDetailView

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
    sysReq_MKS = models.CharField(max_length=30, unique=True)
    title = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return repr(self.sysReq_MKS)+ "  " + self.title

class TestCaseHistory(models.Model):
    def TestCaseHistory(self):
        return self

class TestCase(models.Model):
    testName = models.CharField(max_length=100)
    testedFunctionality = models.CharField(max_length=100)
    testEngineer = models.CharField(max_length=100)
    implementedBy = models.CharField(max_length=100)
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
    version = models.IntegerField(default=1)
    current = models.BooleanField(default=True)
    history = models.ForeignKey(TestCaseHistory)

    class Meta:
        unique_together = ("id", "version")
        ordering = ['version']

    def __str__(self):
        return self.testName
    def TestCase(self):
        return self

class TestStep(models.Model):
    testCase = models.ForeignKey(TestCase, to_field='id', on_delete=models.CASCADE)
    instruction = models.CharField(max_length=500)
    stepOrder = models.IntegerField()
    class Meta:
        unique_together = ("testCase", "stepOrder")
        ordering = ['stepOrder']
    def __str__(self):
        return self.instruction


class ExpectedResult(models.Model):
    testCase = models.ForeignKey(TestCase, to_field='id', on_delete=models.CASCADE)
    expectedResult = models.CharField(max_length=500)
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
        return self.expectedResult

#### Forms

class TestCaseBaseForm(forms.ModelForm):
    numberOfCases = forms.IntegerField()
    class Meta:
        model = TestCase
        exclude = ('testName', 'testSituation', 'status', 'version', 'history')

class TestCaseForm(forms.ModelForm):
    comment = forms.CharField(max_length=300)
    class Meta:
        model = TestCase
        fields = ('systemRequirement', 'testGroup', 'component', 'testedFunctionality', 'testEngineer',
                  'implementedBy', 'testName', 'testSituation', 'status')
    def save(self, commit=True):
        reversion.set_comment(self.cleaned_data['comment'])
        return super(TestCaseForm, self).save(commit=commit)

class TestGroupForm(forms.ModelForm):
    class Meta:
        model = TestGroup
        exclude = ()

class ComponentForm(forms.ModelForm):
    class Meta:
        model = Component
        exclude = ()

class SystemRequirementForm(forms.ModelForm):
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

class TestStepsFormSet(BaseInlineFormSet):
    def clean(self):
        if any(self.errors):
            # Don't bother validating the formset unless each form is valid on its own
            return
        values = set()
        cleaned_data = self.cleaned_data
        for data in cleaned_data:
            value = data.get('stepOrder')
            if value:
                if value in values:
                    raise forms.ValidationError('Duplicate values for Step Order are not allowed.')
                values.add(value)



# Versioning
    reversion.register(TestStep)
    reversion.register(ExpectedResult)
    reversion.register(TestGroup)
    reversion.register(SystemRequirement)
    reversion.register(Component)
    reversion.register(TestCase, follow=["teststep_set", "expectedresult_set"])

