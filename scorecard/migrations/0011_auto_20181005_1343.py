# Generated by Django 2.1.2 on 2018-10-05 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scorecard', '0010_auto_20181004_1413'),
    ]

    operations = [
        migrations.CreateModel(
            name='BusinessUnitGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='businessunit',
            name='bu_group',
            field=models.ForeignKey(null=True, on_delete=models.SET(None), to='scorecard.BusinessUnitGroup'),
        ),
    ]
