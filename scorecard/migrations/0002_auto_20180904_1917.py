# Generated by Django 2.1 on 2018-09-04 23:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scorecard', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='business_unit',
        ),
        migrations.DeleteModel(
            name='BusinessUnit',
        ),
    ]
