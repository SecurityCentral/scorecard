# Generated by Django 2.1.2 on 2018-10-23 18:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scorecard', '0027_auto_20181023_1042'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='securitycapability',
            name='details',
        ),
        migrations.AddField(
            model_name='productsecuritycapability',
            name='details',
            field=models.TextField(blank=True, default=''),
        ),
    ]
