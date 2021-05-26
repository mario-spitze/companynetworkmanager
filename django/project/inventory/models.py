from django.db import models

from networkmap.models import Device
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _

#catalog
class Article(models.Model):
    ean = models.IntegerField()
    name = models.CharField(max_length=26)
    description = models.TextField()
    hardwareClass = models.ForeignKey('HardwareClass',
        models.SET_NULL, null = True)

    class ArticleStatusType(models.TextChoices):
        NEW = 'N', _('new')
        ACTIVE = 'A', _('active')
        OLD = 'O', _('old')

    status = models.CharField(
        max_length=1,
        choices=ArticleStatusType.choices,
        default=ArticleStatusType.NEW
    )

    def __str__(self):
        return self.hardwareClass.__str__() + " : " + self.name

#inventar
class Equipment(models.Model):
    base = models.ForeignKey('Article',
        on_delete=models.CASCADE)
    sn = models.CharField(max_length=20)
    inventarNr = models.CharField(max_length=14)

    def __str__(self):
        return self.base.__str__() + " (" +  self.sn + ")"

class HardwareClass(models.Model):
    name = models.CharField(max_length=20)
    def __str__(self):
        return self.name

class Workplace(models.Model):
    place = models.CharField(max_length=5)
    room = models.CharField(max_length=10)
    def __str__(self):
        return self.room + " - " + self.place

class Customer(models.Model):
    name = models.CharField(max_length=30)
    def __str__(self):
        return self.name

class Handover(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)

    user_object_id = models.IntegerField()
    user_content_type = models.ForeignKey(
        ContentType,
        related_name='user_content',
        on_delete=models.PROTECT,
    )
    user = GenericForeignKey(
        'user_content_type',
        'user_object_id',
    )

    thing_object_id = models.IntegerField(default = -1)
    thing_content_type = models.ForeignKey(
        ContentType,
        related_name='thing_content',
        on_delete=models.PROTECT, blank=True, null=True
    )
    thing = GenericForeignKey(
        'thing_content_type',
        'thing_object_id',
    )

