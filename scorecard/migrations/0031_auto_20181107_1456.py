# Generated by Django 2.1.2 on 2018-11-07 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scorecard', '0030_auto_20181023_1448'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='controlfamily',
            options={'verbose_name_plural': 'control families'},
        ),
        migrations.AlterModelOptions(
            name='productsecuritycapability',
            options={'verbose_name_plural': 'product security capabilities'},
        ),
        migrations.AlterModelOptions(
            name='securitycapability',
            options={'verbose_name_plural': 'security capabilities'},
        ),
        migrations.AlterModelOptions(
            name='securitycategory',
            options={'verbose_name_plural': 'security categories'},
        ),
        migrations.AlterModelOptions(
            name='securitysubcategory',
            options={'verbose_name_plural': 'security subcategories'},
        ),
        migrations.AlterModelOptions(
            name='status',
            options={'verbose_name_plural': 'statuses'},
        ),
        migrations.AddField(
            model_name='buscore',
            name='items_in_progress',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='buscore',
            name='items_supported',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='buscore',
            name='items_total',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='productscore',
            name='items_in_progress',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='productscore',
            name='items_supported',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='productscore',
            name='items_total',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='buscore',
            name='score',
            field=models.IntegerField(default=0, help_text='Integer Field'),
        ),
    ]
