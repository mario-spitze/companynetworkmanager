# Generated by Django 3.1.1 on 2020-09-25 14:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
                ('data', models.JSONField()),
            ],
        ),
        migrations.CreateModel(
            name='PatchField',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('data', models.JSONField()),
            ],
        ),
        migrations.CreateModel(
            name='PatchFieldPort',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
                ('data', models.JSONField()),
                ('classType', models.CharField(choices=[('D', 'Device'), ('T', 'Tunnel')], max_length=1)),
                ('patchFieldPosition', models.IntegerField()),
                ('patchField', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='networkmap.patchfield')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Tunnel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('data', models.JSONField()),
                ('partA', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='partA', to='networkmap.patchfieldport')),
                ('partB', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='partB', to='networkmap.patchfieldport')),
            ],
        ),
        migrations.CreateModel(
            name='DevicePort',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
                ('data', models.JSONField()),
                ('type', models.CharField(choices=[('NET', 'Network'), ('PWR', 'Power'), ('MNG', 'Management')], default='NET', max_length=3)),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='networkmap.device')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Connection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('portA_id', models.PositiveIntegerField()),
                ('portB_id', models.PositiveIntegerField()),
                ('data', models.JSONField()),
                ('portA_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='networkmap_connection_relatedA', related_query_name='networkmap_connections', to='contenttypes.contenttype')),
                ('portB_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='networkmap_connection_relatedB', related_query_name='networkmap_connections', to='contenttypes.contenttype')),
            ],
        ),
    ]