from django import forms
from .models import Devices, DeivceArlam, DeviceEvent

class DevicesForm(forms.ModelForm):
    class Meta:
        model = Devices
        fields = ('id', 'name', 'type', 'owner')

class ArlarmForm(forms.ModelForm):
    class Meta:
        model = DeivceArlam
        fields = ('id', 'device', 'time')

class EventForm(forms.ModelForm):
    class Meta:
        model = DeviceEvent
        fields = ('id', 'device', 'time', 'tag', 'note')