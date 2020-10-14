from django.shortcuts import render

from django.views import generic
from .models import SoftwareInstallation

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

@method_decorator(login_required, name='dispatch')
class LizenzListView(generic.ListView):
    model = SoftwareInstallation
    template_name = 'computer/lizenzList.html'

#    def get_queryset(self):
#        devices = Device.getListWithPortCount()
#        return devices