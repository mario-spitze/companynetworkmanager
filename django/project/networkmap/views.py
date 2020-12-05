from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect

from django.views import generic
from django import forms

from .forms import AddDeviceForm, EditDeviceForm, ConnectDeviceForm
from .models import Device, DevicePort, PatchField, PatchFieldPort
from django.db import transaction
import json


from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

def index(request):
    return HttpResponse("Hello, world. You're at the networkMap index.")


@login_required
def addDevice(request):
    
    if request.method == 'POST':
        
        form = AddDeviceForm(request.POST)
        if form.is_valid():
            d = Device()
            d.name = form.cleaned_data['deviceName']
            x = {}
            d.data = json.dumps(x)
            d.save()
            for i in range(form.cleaned_data['countPorts']):
                p = DevicePort()
                p.PortType = DevicePort.PortType.NETWORK
                p.device = d
                x = {}
                p.data = json.dumps(x)
                p.name = form.cleaned_data['namePorts'].format(i)
                p.save()
            return HttpResponseRedirect('/networkmap/addDevice/')

    else:
        form = AddDeviceForm()

    return render(request, 'networkmap/addDevice.html', {'form': form})

@login_required
def editDevice(request, id):

    if request.method == 'POST':
        form = EditDeviceForm(request.POST)
    #    return HttpResponseRedirect('/networkmap/deviceList/')
    else:
        device = Device.getWithPorts(id)
        form = EditDeviceForm(instance=device)

    return render(request, 'networkmap/editDevice.html', {'form': form, 'id': id})

#class EditDeviceView(generic.FormView):
#    template_name = 'networkmap/editDevice.html'
#    form_class = EditDeviceForm
#    fields = ['name']
#    success_url = '/networkmap/deviceList/'
#    model = Device

#    def get_context_data(self, **kwargs):
#        device = Device.getWithPorts(kwargs.get('id'))
#        return device

@method_decorator(login_required, name='dispatch')
class DeviceListView(generic.ListView):
    model = Device
    template_name = 'networkmap/listDevices.html'

    def get_queryset(self):
        devices = Device.getListWithPortCount()
        return devices

@login_required
def connectPort(request, id_port = -1):

    form = ConnectDeviceForm(request.POST)

    form.fields['fromDevice'].queryset = Device.objects.all()
    form.fields['fromDevicePort'].queryset = DevicePort.objects.all()
    form.fields['toDevice'].queryset = Device.objects.all()
    form.fields['toDevicePort'].queryset = DevicePort.objects.all()
    form.fields['toPatchField'].queryset = PatchField.objects.all()
    form.fields['toPatchFieldPort'].queryset = PatchFieldPort.objects.all()
#    form.fields['toDevice'].widget.is_hidden = True

    return render(request, 'networkmap/connectPort.html', {'form': form})


@login_required
def nextHop(request):
    return render(request, 'networkmap/nextHop.html')


@login_required
def showRoom(request, id_room = -1):

    portForm = forms.Form()
    portForm.fields['Ports'] = forms.ModelChoiceField(label='Port', initial=-1, queryset=None, required=False)
    portForm.fields['Ports'].queryset = PatchFieldPort.objects.all()

    return render(request, 'networkmap/room.html', {'form': portForm})