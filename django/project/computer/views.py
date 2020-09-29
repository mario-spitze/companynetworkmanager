from django.shortcuts import render

from django.views import generic
from .models import SoftwareInstallation
# Create your views here.

class LizenzListView(generic.ListView):
    model = SoftwareInstallation
    template_name = 'computer/lizenzList.html'

#    def get_queryset(self):
#        devices = Device.getListWithPortCount()
#        return devices