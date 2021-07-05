# Generated by Django 3.1.1 on 2021-06-05 21:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0005_auto_20210526_1923'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='ean',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='equipment',
            name='inventarNr',
            field=models.CharField(blank=True, max_length=14, null=True),
        ),
        migrations.AlterField(
            model_name='equipment',
            name='sn',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]