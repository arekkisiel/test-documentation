from django.forms import BaseInlineFormSet
from django import forms
from .models import TestCase, TestGroup, Component, SystemRequirement, ExpectedResult, TestStep

class TestCaseBaseForm(forms.ModelForm):
    numberOfCases = forms.IntegerField()
    class Meta:
        model = TestCase
        exclude = ('testName', 'testSituation', 'status', 'version', 'history', 'testCaseId')

class TestCaseForm(forms.ModelForm):
    class Meta:
        model = TestCase
        fields = ('systemRequirement', 'testGroup', 'component', 'testedFunctionality', 'testEngineer',
                  'implementedBy', 'testName', 'testSituation', 'status')
    def save(self, commit=True):
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