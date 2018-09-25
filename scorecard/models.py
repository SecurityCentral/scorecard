from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=100)
    score = models.IntegerField(default=0)
    max_score = models.IntegerField(default=1)
    percent_score = models.FloatField(default=0)


# OpenControl data
class Standard(models.Model):
    name = models.CharField(max_length=50)
    label = models.CharField(max_length=10)


class ControlFamily(models.Model):
    label = models.CharField(max_length=10)


class Control(models.Model):
    name = models.TextField()
    label = models.CharField(max_length=10)
    family = models.ForeignKey(ControlFamily, on_delete=models.CASCADE)
    standard = models.ForeignKey(Standard, on_delete=models.CASCADE)


class ProductControl(models.Model):
    status = models.CharField(max_length=20)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    control = models.ForeignKey(Control, on_delete=models.CASCADE)

