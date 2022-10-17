from django.db import models
from django.contrib.auth.models import AbstractUser


class UserAddress(models.Model):
    first_line = models.CharField(max_length=255)
    second_line = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=15)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=50)

class HealthCarePlan(models.Model):
    name = models.CharField(max_length=255)

class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', 'admin'
        PATIENT = 'PATIENT', 'patient'
        TECHNICIAN = 'TECHNICIAN', 'TECHNICIAN'

    role = models.CharField(max_length=50, choices=Role.choices)
    health_care_plan = models.ForeignKey(HealthCarePlan, on_delete=models.CASCADE, null=True)
    address = models.ForeignKey(UserAddress, on_delete=models.CASCADE, null=True)
    phone_number = models.CharField(max_length=50)
