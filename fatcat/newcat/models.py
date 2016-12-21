import uuid

from django.db import models

# Create your models here.
from django import forms
from django.forms import widgets


class TestGroup(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
    testGroupName = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.testGroupName

class ExpectedResult(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
    expectedResult = models.CharField(max_length=1000)

    def __str__(self):
        return self

class TestCase(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
    testName = models.CharField(max_length=200)
    testedFunctionality = models.CharField(max_length=200)
    testEngineer = models.CharField(max_length=200)
    implementedBy = models.CharField(max_length=200)
    testSituation = models.CharField(max_length=1000)
    expectedResults = ExpectedResult
    testGroup = models.ForeignKey(TestGroup, to_field='testGroupName',)
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
    id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
    #testCase = models.ManyToOneRel(TestCase, on_delete=models.CASCADE)

    def __str__(self):
        return self

class AddTestCase(forms.ModelForm):
    class Meta:
        model = TestCase
        exclude = ('id',)

class AddTestGroup(forms.ModelForm):
    class Meta:
        model = TestGroup
        exclude = ('id',)