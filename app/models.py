from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

GENDER_CHOICES = (
    ("M", "Male"),
    ("F", "Female"),
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
    ("IN-HOME", "IN-HOME"),
    ("IN-LAB", "IN-LAB"),
)


class User(AbstractUser):
    is_patient = models.BooleanField(default=False)
    is_technician = models.BooleanField(default=False)


class Address(models.Model):
    address_line = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    zipcode = models.IntegerField(max_length=6)
    country = models.CharField(max_length=20, default='Puerto Rico')


# class PaymentMethod(models.Model):


class Patient(models.Model):
    patient_user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    # payment_method =  models.ForeignKey(PaymentMethod, on_delete=models.CASCADE)
    date_of_birth = models.DateTimeField()
    weight = models.IntegerField()
    height = models.IntegerField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    phone_number = models.IntegerField()


class Test(models.Model):
    test_name = models.CharField(max_length=20)
    description = models.CharField(max_length=100)
    requirements = models.CharField(max_length=100)
    locations = models.CharField(choices=LOCATION_CHOICES, max_length=20, default='In-Home')
    price = models.PositiveIntegerField()

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
