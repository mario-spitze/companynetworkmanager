from django.db import models

from networkmap.models import Device
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _, override

class HandoverHelper():
    @property
    def getLastUser(self):
        lastHandover = Handover.objects.filter(
            thing_object_id=self.pk, 
            thing_content_type=ContentType.objects.get_for_model(self)).order_by('timestamp').last()
        if lastHandover==None:
            lastHandover = "neu"
        return lastHandover

#catalog
class Article(models.Model):
    ean = models.BigIntegerField(blank=True, null=True)
    name = models.CharField(max_length=26)
    description = models.TextField(blank=True, null=True)
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

    @property
    def getCount(self):
        if hasattr(self, 'bulkarticle'):
            return self.bulkarticle.stock
        return len(Equipment.objects.filter(base=self.pk))


    @property
    def getType(self):
        if hasattr(self, 'bulkarticle'):
            return "bulkart"
        return "indart"

    def __str__(self):
        return self.hardwareClass.__str__() + " : " + self.name

class BulkArticle(Article, HandoverHelper):
    stock = models.IntegerField(default=0)

#inventar
class Equipment(models.Model, HandoverHelper):
    base = models.ForeignKey('Article',
        on_delete=models.CASCADE)
    sn = models.CharField(max_length=40, blank=True, null=True)
    inventarNr = models.CharField(max_length=14, blank=True, null=True)

    def __str__(self):
        output = self.base.__str__()
        if self.sn:
            output = output + " (" +  self.sn + ")"
        return output

    @property
    def getType(self):
        return "equipment"

class HardwareClass(models.Model):
    name = models.CharField(max_length=20)
    def __str__(self):
        return self.name

class Workplace(models.Model):
    room = models.CharField(max_length=10)
    place = models.CharField(max_length=5)
    customer = models.ForeignKey('Customer',
        models.SET_NULL, null = True, blank=True)
    comment = models.TextField(blank=True, null=True)
    def __str__(self):
        return self.room + " - " + self.place

class Customer(models.Model):
    name = models.CharField(max_length=30)
    def __str__(self):
        return self.name


class Handover(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)

    class MovementType(models.IntegerChoices):
        LAY = 21
        LAYBACK = 22

    movementType = models.IntegerField(
        choices=MovementType.choices,
        default=MovementType.LAY
    )

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

    oppositeHandover = models.ForeignKey('Handover',
        models.SET_NULL, null = True)

    def getThing(self):
        thing = None
        if self.thing_content_type == ContentType.objects.get_for_model(Equipment):
            thing = Equipment.objects.get(id=self.thing_object_id)
        else:
            thing = BulkArticle.objects.get(id=self.thing_object_id)
        return thing

    def getPlace(self):
        place = None
        if self.user_content_type == ContentType.objects.get_for_model(Workplace):
            place = Workplace.objects.get(id=self.user_object_id)
        else:
            place = Customer.objects.get(id=self.user_object_id)
        return place

    def __str__(self):
        output = self.thing.__str__()
        if self.movementType == Handover.MovementType.LAY:
            output = output + _(' laid to ').__str__()
        else:
            output = output + _(' laid back from ').__str__()
        output = output + self.user.__str__() + " (" + str(self.pk) + ")"

        return output
