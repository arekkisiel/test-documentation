import uuid

from django.db import models

# Create your models here.

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

