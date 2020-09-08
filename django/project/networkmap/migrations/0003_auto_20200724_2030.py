# Generated by Django 3.0.4 on 2020-07-24 20:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('networkmap', '0002_auto_20200408_1549'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='deviceport',
            name='classType',
        ),
        migrations.AlterField(
            model_name='deviceport',
            name='device',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='networkmap.Device'),
        ),
    ]
