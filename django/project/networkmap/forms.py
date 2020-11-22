from django import forms
from .models import Device
from django.db.models.query import EmptyQuerySet

class AddDeviceForm(forms.Form):
    deviceName = forms.CharField(label='Name', max_length=40)
    countPorts = forms.IntegerField(label='Anzahl Ports')
    namePorts = forms.CharField(label='PortBezeichnung', help_text='Port{}', initial='Port{}')

class EditDeviceForm(forms.ModelForm):
#    name = forms.CharField(label='Name', max_length=40)

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')
        super(EditDeviceForm, self).__init__(*args, **kwargs)
        if instance is not None:
            counter = 1
            for devicePort in instance.deviceport_set.all():
                help_text_content = ("DB Port-ID: %s", devicePort.id)
                self.fields['devicePortName-' + str(counter)] = forms.CharField(label="Port", initial=devicePort.name, help_text=devicePort.id)
                counter += 1

class ConnectDeviceForm(forms.Form):
    fromDevice = forms.ModelChoiceField(label='Von Gerät', initial=-1, queryset=None, required=False, widget=forms.Select(attrs={"onChange":'refresh()'}))
    fromDevicePort = forms.ModelChoiceField(label='Von Port', initial=-1, queryset=None, required=False)
    toDevice = forms.ModelChoiceField(label='Nach Gerät', initial=-1, queryset=None, required=False)
    toDevicePort = forms.ModelChoiceField(label='Nach Port', initial=-1, queryset=None, required=False)
    toPatchField = forms.ModelChoiceField(label='Nach Patchfeld', initial=-1, queryset=None, required=False)
    toPatchFieldPort = forms.ModelChoiceField(label='Nach Port', initial=-1, queryset=None, required=False)
