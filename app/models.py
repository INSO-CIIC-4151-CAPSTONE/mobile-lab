from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser


GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
)

STATUS_CHOICES = (
    ('Pending', 'Pending'),
    ('On The Way', 'LabTech on the way'),
    ('In Process', 'Analyzing Results'),
    ('Completed', 'Blood sample taken '),
    ('Results Available', 'Results Available'),
    ('Cancelled', 'Cancelled')
)

LOCATION_CHOICES = (
    ('IN-HOME', 'IN-HOME'),
    ('IN-LAB', 'IN-LAB'),
)

USER_ROLE_CHOICES = (
    ('ADMIN', 'admin'),
    ('PATIENT', 'Patient')
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

# class PaymentMethod(models.Model):


class HealthCarePlan(models.Model):
    name = models.CharField(max_length=255)


class User(AbstractUser):
    role = models.CharField(max_length=50, choices=USER_ROLE_CHOICES)
    health_care_plan = models.ForeignKey(HealthCarePlan, on_delete=models.CASCADE, null=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, null=True)
    phone_number = models.CharField(max_length=50)
    employer_lab = models.ForeignKey(Laboratory, on_delete=models.CASCADE, null=True)


class Test(models.Model):
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=500)
    requirements = models.CharField(max_length=500)
    locations = models.CharField(choices=LOCATION_CHOICES, max_length=20, default='In-Home')
    laboratory = models.ForeignKey(Laboratory, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.test_name


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.user)

    @property
    def total_cost(self):
        return self.quantity * self.test.price


class Order(models.Model):
    order_id = models.PositiveIntegerField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=STATUS_CHOICES, max_length=50, default='Pending')


class PatientTest(models.Model):
    patient_user = models.OneToOneField(User, on_delete=models.CASCADE)
    orders = models.ForeignKey(Order, on_delete=models.CASCADE)


# class Appointment(models.Model): Still thinking how to implement it or if we need it. We can use django-scheduler app


class Technician(models.Model):
    technician_user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    phone_number = models.IntegerField()
    employee_code = models.CharField(max_length=10)


class Laboratory(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    technicians = models.ForeignKey(Technician, on_delete=models.CASCADE)

class Request(models.Model):
    lab_test = models.ForeignKey(Test, on_delete=models.CASCADE)
    patient = models.ForeignKey(User, related_name='patient', on_delete=models.CASCADE)
    lab_technician = models.ForeignKey(User, related_name='lab_technician', on_delete=models.CASCADE)
    test_status = models.CharField(max_length=50, choices=REQUEST_STATUS_CHOICES)

class TestResult(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
