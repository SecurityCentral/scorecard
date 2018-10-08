from django.db import models


class BusinessUnitGroup(models.Model):
    name = models.CharField(max_length=100, default='')
    pp_id = models.IntegerField(default=0)


class BusinessUnit(models.Model):
    name = models.CharField(max_length=100, default='')
    bu_group = models.ForeignKey(BusinessUnitGroup, on_delete=models.SET(None), null=True)
    pp_id = models.IntegerField(default=0)


class Person(models.Model):
    full_name = models.CharField(max_length=100, default='')
    email = models.EmailField(default='')
    username = models.CharField(max_length=100, default='')
    pp_id = models.IntegerField(default=0)


class Product(models.Model):
    name = models.CharField(max_length=100)
    score = models.IntegerField(default=0)
    max_score = models.IntegerField(default=1)
    percent_score = models.FloatField(default=0)
    business_unit = models.ForeignKey(BusinessUnit, on_delete=models.SET(None), null=True)
    pp_id = models.IntegerField(default=0)


class ProductRole(models.Model):
    description = models.CharField(max_length=200, default='')
    product = models.ForeignKey(Product, on_delete=models.SET(None), null=True)
    person = models.ForeignKey(Person, on_delete=models.SET(None), null=True)


class SecurityCapability(models.Model):
    name = models.CharField(max_length=200, default='')
    supporting_controls = models.CharField(max_length=200, blank=True)


class Status(models.Model):
    name = models.CharField(max_length=50, default='')
    value = models.IntegerField(default=0)


class SecurityCapabilityProduct(models.Model):
    status = models.ForeignKey(Status, blank=True, on_delete=models.SET(''))
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    security_capability = models.ForeignKey(SecurityCapability, on_delete=models.CASCADE)


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

