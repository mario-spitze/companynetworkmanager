# Generated by Django 3.2.8 on 2022-01-05 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0012_alter_equipment_sn'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='ean',
            field=models.BigIntegerField(blank=True, null=True),
        ),
    ]
