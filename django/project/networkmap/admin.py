from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(Device)
admin.site.register(DevicePort)
admin.site.register(PatchFieldPort)
admin.site.register(PatchField)
admin.site.register(Tunnel)
admin.site.register(Connection)

