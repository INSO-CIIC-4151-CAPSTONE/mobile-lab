from django.forms import ModelForm

from .models import *


class PatientForm(ModelForm):
    class Meta:
        model = User
        fields = ['gender', 'phone_number', 'profile_picture']


class AddressForm(ModelForm):
    class Meta:
        model = Address
        fields = '__all__'


class HealthForm(ModelForm):
    class Meta:
        model = HealthCarePlan
        fields = '__all__'
