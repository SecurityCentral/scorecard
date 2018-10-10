# Generated by Django 2.1.2 on 2018-10-08 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scorecard', '0012_auto_20181005_1405'),
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(default='', max_length=100)),
                ('email', models.EmailField(default='', max_length=254)),
                ('pp_id', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='ProductRole',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(default='', max_length=200)),
                ('person', models.ForeignKey(null=True, on_delete=models.SET(None), to='scorecard.Person')),
                ('product', models.ForeignKey(null=True, on_delete=models.SET(None), to='scorecard.Product')),
            ],
        ),
    ]