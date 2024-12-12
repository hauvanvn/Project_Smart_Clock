from django import forms
from .models import Devices

class DevicesForm(forms.ModelForm):
    class Meta:
        model = Devices
        fields = (
            'id',
            'name',
            'type',
            'owner'
        )