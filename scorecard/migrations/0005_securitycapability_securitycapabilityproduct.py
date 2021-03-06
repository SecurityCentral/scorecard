# Generated by Django 2.1 on 2018-09-27 15:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scorecard', '0004_product_percent_score'),
    ]

    operations = [
        migrations.CreateModel(
            name='SecurityCapability',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='SecurityCapabilityProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=20)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scorecard.Product')),
                ('security_capability', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scorecard.SecurityCapability')),
            ],
        ),
    ]
