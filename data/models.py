from django.db import models


class TestResult(models.Model):
    session_id = models.CharField(max_length=255, blank=False, null=True, unique=True)
    age = models.IntegerField(blank=False, null=True)
    gender = models.CharField(max_length=10, blank=False, null=True)
    speciality = models.CharField(max_length=30, blank=False, null=True)
    city = models.CharField(max_length=30, blank=False, null=True)
    test1 = models.IntegerField(default=0, null=True)
    test2 = models.IntegerField(default=0, null=True)
    test3 = models.IntegerField(default=0, null=True)