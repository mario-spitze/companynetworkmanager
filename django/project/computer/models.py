from django.db import models
from networkmap.models import Device

from django.utils.translation import gettext_lazy as _

class Device(models.Model):
    deviceName = models.CharField(max_length=26)
    networkDevice = models.OneToOneField('networkmap.Device',
        on_delete=models.CASCADE)

    inventNumber = models.IntegerField()

    def __str__(self):
        return self.deviceName

class Software(models.Model):
    softwareName = models.CharField(max_length=20)
    publisher = models.CharField(max_length=20)

    def __str__(self):
        return self.softwareName

class SoftwareInstallation(models.Model):
    version = models.CharField(max_length=10)
    software = models.ForeignKey('Software',
        on_delete=models.CASCADE)
    device = models.ForeignKey('Device',
        on_delete=models.CASCADE)
    key = models.CharField(max_length=30)
    class SoftwareType(models.TextChoices):
        DEVICE = 'O', _('OS')
        TUNNEL = 'N', _('normal')

    softwareType = models.CharField(
        max_length=1,
        choices=SoftwareType.choices,
    )

    def __str__(self):
        return self.software + " Version " + version + " on " + device

#class OS(models.Model):
#    oSName = models.CharField(max_length=20)
#
#    def __str__(self):
#        return self.oSName