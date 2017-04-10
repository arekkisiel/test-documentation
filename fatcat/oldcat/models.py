import uuid

from django.db import models

# Create your models here.

class OldCase(models.Model):
    id = int
    testCaseUUID = models.UUIDField(default=uuid.uuid4, editable=False)
    systemRequirement = models.TextField()
    testUnit = models.TextField()
    testName = models.TextField()
    implementedBy = models.TextField()
    testSituation = models.TextField()
    testCase = models.TextField()
    preconditions = models.TextField()
    functionalSteps = models.TextField()
    additionalInfo = models.TextField()
    expectedResults = models.TextField()
    filename = models.TextField()
    version = models.IntegerField(default=1)
    current = models.BooleanField(default=True)

    def __str__(self):
        return self

