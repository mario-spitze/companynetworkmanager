from django.contrib import admin

# Register your models here.

from .models import *


admin.site.register(Device)
admin.site.register(Software)
admin.site.register(SoftwareInstallation)
admin.site.register(DeviceModel)