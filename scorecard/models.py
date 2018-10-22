from django.db import models


class BusinessUnitGroup(models.Model):
    name = models.CharField(max_length=100, default='')
    pp_id = models.IntegerField(default=0)


class BusinessUnit(models.Model):
    name = models.CharField(max_length=100, default='')
    bu_group = models.ForeignKey(BusinessUnitGroup, on_delete=models.SET(None), null=True)
    pp_id = models.IntegerField(default=0)


class BUScore(models.Model):
    score = models.IntegerField(default=0)
    max_score = models.IntegerField(default=1)
    bu = models.ForeignKey(BusinessUnit, on_delete=models.CASCADE, null=True)

    def percent(self):
        if self.max_score < 1:
            self.max_score = 1
        return round(self.score * 100 / self.max_score, 1)


class Person(models.Model):
    full_name = models.CharField(max_length=100, default='')
    email = models.EmailField(default='')
    username = models.CharField(max_length=100, default='')
    pp_id = models.IntegerField(default=0)


class Product(models.Model):
    name = models.CharField(max_length=100)
    business_unit = models.ForeignKey(BusinessUnit, on_delete=models.SET(None), null=True)
    published = models.BooleanField(default=False)
    pp_id = models.IntegerField(default=0)


class ProductScore(models.Model):
    category = models.CharField(max_length=100, default='')
    score = models.IntegerField(default=0)
    max_score = models.IntegerField(default=1)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)

    def percent(self):
        return round(self.score * 100 / self.max_score, 1)


class SecurityRole(models.Model):
    description = models.CharField(max_length=200, default='', blank=True)
    function = models.CharField(max_length=200, default='', blank=True)


class ProductSecurityRole(models.Model):
    role = models.ForeignKey(SecurityRole, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET(None), null=True)
    person = models.ForeignKey(Person, on_delete=models.SET(None), null=True)


class SecurityCategory(models.Model):
    name = models.CharField(max_length=100, default='')


class SecuritySubCategory(models.Model):
    name = models.CharField(max_length=100, default='')


class SecurityCapability(models.Model):
    name = models.CharField(max_length=200, default='')
    supporting_controls = models.CharField(max_length=200, blank=True)
    details = models.TextField(default='', blank=True)
    category = models.ForeignKey(SecurityCategory, on_delete=models.SET(''), null=True)
    sub_category = models.ForeignKey(SecuritySubCategory, on_delete=models.SET(''), null=True)


class Status(models.Model):
    name = models.CharField(max_length=50, default='')
    value = models.IntegerField(default=0)


class ProductSecurityCapability(models.Model):
    status = models.ForeignKey(Status, null=True, on_delete=models.SET(''))
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

