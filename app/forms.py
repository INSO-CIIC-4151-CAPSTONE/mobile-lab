from django.forms import ModelForm
from .models import Request


class RequestForm(ModelForm):
    class Meta:
        model = Request
        fields = ['patient', 'lab_test', 'modality', 'date_and_time', 'comments']
