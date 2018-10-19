from django.contrib import admin
from .models import BusinessUnit, BusinessUnitGroup, BUScore, Control, ControlFamily, Person, Product, ProductScore, \
    ProductSecurityRole, ProductControl, ProductSecurityCapability, SecurityCapability, SecurityRole, Standard, Status


class BusinessUnitAdmin(admin.ModelAdmin):
    list_display = ('name', 'bu_group', 'pp_id')


class BusinessUnitGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'pp_id')


class BUScoreAdmin(admin.ModelAdmin):
    list_display = ('score', 'max_score', 'bu')


class ControlAdmin(admin.ModelAdmin):
    list_display = ('name', 'label', 'family', 'standard')


class ControlFamilyAdmin(admin.ModelAdmin):
    list_display = ('label',)


class PersonAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'username', 'pp_id')


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'business_unit', 'pp_id')


class ProductScoreAdmin(admin.ModelAdmin):
    list_display = ('category', 'score', 'max_score', 'product')


class ProductRoleAdmin(admin.ModelAdmin):
    list_display = ('role', 'product', 'person')


class ProductControlAdmin(admin.ModelAdmin):
    list_display = ('status', 'product', 'control')


class ProductSecurityCapabilityAdmin(admin.ModelAdmin):
    list_display = ('status', 'product', 'security_capability')


class SecurityCapabilityAdmin(admin.ModelAdmin):
    list_display = ('name', 'supporting_controls')


class SecurityRoleAdmin(admin.ModelAdmin):
    list_display = ('description', 'function')


class StandardAdmin(admin.ModelAdmin):
    list_display = ('name', 'label')


class StatusAdmin(admin.ModelAdmin):
    list_display = ('name', 'value')


admin.site.register(BusinessUnit, BusinessUnitAdmin)
admin.site.register(BusinessUnitGroup, BusinessUnitGroupAdmin)
admin.site.register(BUScore, BUScoreAdmin)
admin.site.register(Control, ControlAdmin)
admin.site.register(ControlFamily, ControlFamilyAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductScore, ProductScoreAdmin)
admin.site.register(ProductSecurityRole, ProductRoleAdmin)
admin.site.register(ProductControl, ProductControlAdmin)
admin.site.register(ProductSecurityCapability, ProductSecurityCapabilityAdmin)
admin.site.register(SecurityCapability, SecurityCapabilityAdmin)
admin.site.register(SecurityRole, SecurityRoleAdmin)
admin.site.register(Standard, StandardAdmin)
admin.site.register(Status, StatusAdmin)
