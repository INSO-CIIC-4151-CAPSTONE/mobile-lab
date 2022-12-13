import datetime


from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from django.forms import ModelForm

from .models import *

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


class UpdateRequestForm(forms.Form):
    date = forms.DateField(widget=forms.DateInput(attrs={
        'class': 'form-control'
    }), label='Date')
    hour = forms.TimeField(widget=forms.TimeInput(attrs={
        'class': 'form-control'
    }), label='Hour')
    comments = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
        'rows': 3
    }), max_length=1024, label='Comments')
    modality = forms.ChoiceField(widget=forms.Select(attrs={
        'class': 'form-control'
    }), choices=MODALITY_CHOICES, label='Modality')
    status = forms.ChoiceField(widget=forms.Select(attrs={
        'class': 'form-control'
    }), choices=STATUS_CHOICES, label='Status')
    accepted = forms.BooleanField(widget=forms.CheckboxInput(attrs={
        'class': 'form-control'
    }), label='Accept Request', required=False)

    def clean_date(self):
        data = self.cleaned_data['date']

        # Check if a date is not in the past.
        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - renewal in past'))

        # Check if a date is in the allowed range (+52 weeks from today).
        if data > datetime.date.today() + datetime.timedelta(weeks=52):
            raise ValidationError(_('Invalid date - date more than 52 weeks ahead'))

        # Remember to always return the cleaned data.
        return data


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'gender', 'email', 'phone_number', 'profile_picture']


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
