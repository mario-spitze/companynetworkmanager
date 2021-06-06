from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(Article)
admin.site.register(BulkArticle)
admin.site.register(Equipment)
admin.site.register(HardwareClass)
admin.site.register(Workplace)
admin.site.register(Customer)
admin.site.register(Handover)
