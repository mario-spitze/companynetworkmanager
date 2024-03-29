# Generated by Django 3.1.1 on 2021-06-06 18:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0006_auto_20210605_2152'),
    ]

    operations = [
        migrations.CreateModel(
            name='BulkArticle',
            fields=[
                ('article_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='inventory.article')),
                ('stock', models.IntegerField(default=0)),
            ],
            bases=('inventory.article',),
        ),
    ]
