from django.db import models
from django.contrib.auth.models import AbstractUser


class Laboratory(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100)
    address = models.CharField(max_length=100)

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
    employer_lab = models.ForeignKey(Laboratory, on_delete=models.CASCADE, null=True)

class LabTest(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    requirements = models.CharField(max_length=500)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    laboratory = models.ForeignKey(Laboratory, on_delete=models.CASCADE)

class TestRequest(models.Model):
    class Status(models.TextChoices):
        # define here some better states states
        ACCEPTED = 'ACCEPTED', 'accepted'
        DECLINED = 'DECLINED', 'declined'
        PENDING = 'PENDING', 'pending'

    lab_test = models.ForeignKey(LabTest, on_delete=models.CASCADE)
    patient = models.ForeignKey(User, related_name='patient', on_delete=models.CASCADE)
    lab_technician = models.ForeignKey(User, related_name='lab_technician', on_delete=models.CASCADE)
    test_status = models.CharField(max_length=50, choices=Status.choices)

class TestResult(models.Model):
    lab_test = models.ForeignKey(LabTest, on_delete=models.CASCADE)

class Appointment(models.Model):
    date = models.DateField(null=False)
    time = models.TimeField(null=False)
    laboratory = models.ForeignKey(Laboratory, on_delete=models.CASCADE)
    lab_test = models.ForeignKey(LabTest, on_delete=models.CASCADE)
    lab_test_request = models.ForeignKey(TestRequest, on_delete=models.CASCADE)


