import uuid

from django.db import models

# Create your models here.
class TestGroup(models.Model):
    testGroupName = models.CharField(max_length=200)

class ExpectedResult(models.Model):
    id = models.UUIDField
    expectedResult = models.CharField(max_length=1000)

class TestCase(models.Model):
    #id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
    testName = models.CharField(max_length=200)
    testGroup = TestGroup
    testedFunctionality = models.CharField(max_length=200)
    testEngineer = models.CharField(max_length=200)
    implementedBy = models.CharField(max_length=200)
    testSituation = models.CharField(max_length=1000)
    expectedResults = ExpectedResult
    status = models.CharField(max_length=200)

class TestStep(models.Model):
    id = models.UUIDField
    #testCase = models.ManyToOneRel(TestCase, on_delete=models.CASCADE)

class OldCase(models.Model):
    id = int
    system_requirements = models.TextField()
    test_unit = models.TextField()
    test_id = models.TextField()
    implemented = models.TextField()
    test_situation = models.TextField()
    test_case = models.TextField()
    precondition = models.TextField()
    functional_steps = models.TextField()
    additional_info = models.TextField()
    expected_result = models.TextField()
    filename = models.TextField()

    def __str__(self):
        return self

