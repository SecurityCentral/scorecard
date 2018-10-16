# Generated by Django 2.1.2 on 2018-10-15 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scorecard', '0016_auto_20181010_1525'),
    ]

    operations = [
        migrations.AddField(
            model_name='businessunit',
            name='max_score',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='businessunit',
            name='percent_score',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='businessunit',
            name='score',
            field=models.IntegerField(default=0),
        ),
    ]