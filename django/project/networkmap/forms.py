from django import forms
from .models import Device

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

#    def __init__(self, *args, **kwargs):
#    questions = kwargs.pop('questions')
#        super(EditDeviceForm, self).__init__(*args, **kwargs)
#    counter = 1
#    for q in questions:
#        self.fields['question-' + str(counter)] = forms.CharField(label=question)
#        counter += 1

