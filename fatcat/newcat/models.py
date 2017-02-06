from django.db import models

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

class TestCaseId(models.Model):
    def TestCaseId(self):
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
    testCaseId = models.ForeignKey(TestCaseId)

    class Meta:
        ordering = ['-version']

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


