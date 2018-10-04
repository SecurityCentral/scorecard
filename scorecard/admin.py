from django.contrib import admin
from .models import BusinessUnit, Control, ControlFamily, Product, ProductControl, SecurityCapability, \
    SecurityCapabilityProduct, Standard, Status


class BusinessUnitAdmin(admin.ModelAdmin):
    list_display = ('name',)


class ControlAdmin(admin.ModelAdmin):
    list_display = ('name', 'label', 'family', 'standard')


class ControlFamilyAdmin(admin.ModelAdmin):
    list_display = ('label',)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'score', 'max_score', 'percent_score', 'business_unit')


class ProductControlAdmin(admin.ModelAdmin):
    list_display = ('status', 'product', 'control')


class SecurityCapabilityAdmin(admin.ModelAdmin):
    list_display = ('name', 'supporting_controls')


class SecurityCapabilityProductAdmin(admin.ModelAdmin):
    list_display = ('status', 'product', 'security_capability')


class StandardAdmin(admin.ModelAdmin):
    list_display = ('name', 'label')


class StatusAdmin(admin.ModelAdmin):
    list_display = ('name', 'value')


admin.site.register(BusinessUnit, BusinessUnitAdmin)
admin.site.register(Control, ControlAdmin)
admin.site.register(ControlFamily, ControlFamilyAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductControl, ProductControlAdmin)
admin.site.register(SecurityCapability, SecurityCapabilityAdmin)
admin.site.register(SecurityCapabilityProduct, SecurityCapabilityProductAdmin)
admin.site.register(Standard, StandardAdmin)
admin.site.register(Status, StatusAdmin)
