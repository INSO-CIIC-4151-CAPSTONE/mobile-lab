from django.forms import ModelForm, ImageField
from .models import *


class RequestForm(ModelForm):
    class Meta:
        model = Request
        fields = ['patient', 'lab_test', 'modality', 'date_and_time', 'comments']

class UserProfileForm(ModelForm):
    ppic = ImageField()
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'gender', 'email', 'phone_number', 'ppic']