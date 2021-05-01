from django.db import models

from networkmap.models import Device

from django.utils.translation import gettext_lazy as _

#catalog
class Article(models.Model):
    ean = models.IntegerField()
    name = models.CharField(max_length=26)
    description = models.TextField()
    class ArticleStatusType(models.TextChoices):
        NEW = 'N', _('new')
        ACTIVE = 'A', _('active')
        OLD = 'O', _('old')

    status = models.CharField(
        max_length=1,
        choices=ArticleStatusType.choices,
        default=ArticleStatusType.NEW
    )

#inventar
class Equipment(models.Model):
    base = models.ForeignKey('Article',
        on_delete=models.CASCADE)
    sn = models.CharField(max_length=20)
    inventarNr = models.CharField(max_length=14)

