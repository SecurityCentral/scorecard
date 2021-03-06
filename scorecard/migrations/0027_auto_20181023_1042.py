# Generated by Django 2.1.2 on 2018-10-23 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scorecard', '0026_auto_20181022_1231'),
    ]

    operations = [
        migrations.AlterField(
            model_name='securitycapability',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=models.SET(''), to='scorecard.SecurityCategory'),
        ),
        migrations.AlterField(
            model_name='securitycapability',
            name='sub_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=models.SET(''), to='scorecard.SecuritySubCategory'),
        ),
    ]
