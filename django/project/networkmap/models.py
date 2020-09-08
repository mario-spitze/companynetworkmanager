from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.fields import JSONField

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

import json 

# Create your models here.

class Device(models.Model):
    name = models.CharField(max_length=40)
    data = JSONField()
    def __str__(self):
        return self.name
    
    def getList():
        return Device.objects.all()

    def getListWithPortCount():
        deviceList = Device.getList()
        for device in deviceList:
            device.portCount = DevicePort.objects.filter(device=device.id).count()
        return deviceList
    
    def getListWithPorts():
        deviceList = Device.getList()
        return deviceList
    
    def getWithPorts(searchId):
        device = Device.objects.filter(id=searchId).first()
        return device

class Port(models.Model):
    name = models.CharField(max_length=40)
    data = JSONField()
    
    class PortClass(models.TextChoices):
        DEVICE = 'D', _('Device')
        TUNNEL = 'T', _('Tunnel')

    classType = models.CharField(
        max_length=1,
        choices=PortClass.choices,
    )
    class Meta:
        abstract = True

class DevicePort(Port):
    classType = Port.PortClass.DEVICE

    device = models.ForeignKey(
        'Device',
        on_delete=models.CASCADE,
    )

    class PortType(models.TextChoices):
        NETWORK = 'NET', _('Network')
        POWER = 'PWR', _('Power')
        MNG = 'MNG', _('Management')
    type = models.CharField(
        max_length=3,
        choices=PortType.choices,
        default=PortType.NETWORK,
    )

    def __str__(self):
        return self.name

#    def __init__(self):
#        super().__init__(self)
#        self.classType = Port.PortClass.DEVICE


class PatchFieldPort(Port):
    patchField = models.ForeignKey(
        'PatchField',
        on_delete=models.CASCADE
    )   
    patchFieldPosition = models.IntegerField()
#    def __init__(self):
#        self.classType = Port.PortClass.TUNNEL
#        super().__init__(self)

class PatchField(models.Model): 
    name = models.CharField(max_length=20)
    data = JSONField()

class Tunnel(models.Model):
    name = models.CharField(max_length=20)
    partA = models.ForeignKey(
        'PatchFieldPort',
        on_delete=models.CASCADE,
        related_name='partA'
    )
    partB = models.ForeignKey(
        'PatchFieldPort',
        on_delete=models.CASCADE,
        related_name='partB'
    )
    data = JSONField()

class Connection(models.Model):

    portA_id = models.PositiveIntegerField()
    portA_type = models.ForeignKey(ContentType, on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_relatedA",
        related_query_name="%(app_label)s_%(class)ss")

    partA = GenericForeignKey('portA_type', 'portA_id')


    portB_id = models.PositiveIntegerField()
    portB_type = models.ForeignKey(ContentType, on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_relatedB",
        related_query_name="%(app_label)s_%(class)ss")

    partB = GenericForeignKey('portB_type', 'portB_id')

#    partB = models.ForeignKey(
#        'Port',
#        on_delete=models.CASCADE,
#        related_name='partB'
#    )
    data = JSONField()