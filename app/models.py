from email.policy import default
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

''' © 2022 Mobile-Lab, All Rights Reserved. '''

GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female')
)

STATUS_CHOICES = (
    ('Pending', 'Pending'),
    ('On The Way', 'LabTech on the way'),
    ('In Process', 'Analyzing Results'),
    ('Completed', 'Blood sample taken '),
    ('Results Available', 'Results Available'),
    ('Cancelled', 'Cancelled')
)

MODALITY_CHOICES = (
    ('IN-HOME', 'IN-HOME'),
    ('IN-LAB', 'IN-LAB')
)

USER_ROLE_CHOICES = (
    ('ADMIN', 'admin'),
    ('PATIENT', 'Patient'),
    ('TECHNICIAN', 'Technician')
)

REQUEST_STATUS_CHOICES = (
    ('APROVED', 'Aproved'),
    ('DECLINED', 'Declined'),
    ('PENDING', 'Pending')
)


class Address(models.Model):
    first_line = models.CharField(max_length=200)
    second_line = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    zip_code = models.CharField(max_length=15)
    country = models.CharField(max_length=20, default='Puerto Rico')
    state = models.CharField(max_length=50)


class Laboratory(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100)
    address = models.CharField(max_length=100)


class HealthCarePlan(models.Model):
    name = models.CharField(max_length=255)
    card_front = models.ImageField(upload_to='insurance_cards_images/')
    card_back = models.ImageField(upload_to='insurance_cards_images/')


class User(AbstractUser):
    role = models.CharField(max_length=50, choices=USER_ROLE_CHOICES, blank=True, default='PATIENT')
    health_care_plan = models.ForeignKey(HealthCarePlan, on_delete=models.CASCADE, null=True, blank=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, null=True, blank=True)
    phone_number = models.CharField(max_length=50, null=True, blank=True)
    employer_lab = models.ForeignKey(Laboratory, on_delete=models.CASCADE, null=True, blank=True)
    gender = models.CharField(max_length=50, choices=GENDER_CHOICES, default='', null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_images/', null=True, blank=True)


class Card(models.Model):
    stride_token = models.CharField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Test(models.Model):
    name = models.CharField(max_length=500)
    description = models.CharField(max_length=5000)
    requirements = models.CharField(max_length=1500)
    laboratory = models.ForeignKey(Laboratory, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=6, decimal_places=2)


class Request(models.Model):
    requested_date = models.DateTimeField(auto_now_add=True)
    lab_test = models.ForeignKey(Test, null=True, on_delete=models.CASCADE)
    date = models.DateField(default='00/00/0000')
    hour = models.TimeField()
    patient = models.ForeignKey(User, related_name='request_patient', on_delete=models.CASCADE)
    technician = models.ForeignKey(User, related_name='request_technician', null=True, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=REQUEST_STATUS_CHOICES, default='PENDING')
    comments = models.CharField(max_length=1024, default='')
    modality = models.CharField(max_length=50, choices=MODALITY_CHOICES, default='IN-HOME')


class Appointment(models.Model):
    date_and_time = models.DateTimeField()  # YYYY-MM-DD HH:MM
    patient = models.ForeignKey(User, related_name='appointment_patient', on_delete=models.CASCADE)
    technician = models.ForeignKey(User, related_name='appointment_technician', on_delete=models.CASCADE)
    laboratory = models.ForeignKey(Laboratory, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    request = models.ForeignKey(Request, on_delete=models.CASCADE)
    comments = models.CharField(max_length=1024, default='')
    status = models.CharField(choices=STATUS_CHOICES, max_length=50, default='Pending')
    modality = models.CharField(max_length=50, choices=MODALITY_CHOICES, default='IN-HOME')


class TestResult(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)


class Message(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    message = models.CharField(max_length=4000)
