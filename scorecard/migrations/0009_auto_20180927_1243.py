# Generated by Django 2.1 on 2018-09-27 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scorecard', '0008_auto_20180927_1243'),
    ]

    operations = [
        migrations.AlterField(
            model_name='status',
            name='name',
            field=models.CharField(default='', max_length=50),
        ),
    ]