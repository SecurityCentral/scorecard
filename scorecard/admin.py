from django.contrib import admin
from scorecard import models


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
    list_display = ('name', 'business_unit', 'published', 'pp_id')


class ProductScoreAdmin(admin.ModelAdmin):
    list_display = ('category', 'score', 'max_score', 'product')


class ProductRoleAdmin(admin.ModelAdmin):
    list_display = ('role', 'product', 'person')


class ProductControlAdmin(admin.ModelAdmin):
    list_display = ('status', 'product', 'control')


class ProductSecurityCapabilityAdmin(admin.ModelAdmin):
    list_display = ('id', 'status__name', 'product__name', 'security_capability__name',
                    'security_capability__category', 'details')
    list_filter = ('product__name', 'security_capability__category__name')

    def status__name(self, obj):
        return obj.status.name

    def product__name(self, obj):
        return obj.product.name

    def security_capability__name(self, obj):
        return obj.security_capability.name

    def security_capability__category(selfs, obj):
        return obj.security_capability.category.name


class SecurityCapabilityAdmin(admin.ModelAdmin):
    list_display = ('name', 'supporting_controls', 'category', 'sub_category')


class SecurityCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


class SecuritySubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


class SecurityRoleAdmin(admin.ModelAdmin):
    list_display = ('description', 'function')


class StandardAdmin(admin.ModelAdmin):
    list_display = ('name', 'label')


class StatusAdmin(admin.ModelAdmin):
    list_display = ('name', 'value')


admin.site.register(models.BusinessUnit, BusinessUnitAdmin)
admin.site.register(models.BusinessUnitGroup, BusinessUnitGroupAdmin)
admin.site.register(models.BUScore, BUScoreAdmin)
admin.site.register(models.Control, ControlAdmin)
admin.site.register(models.ControlFamily, ControlFamilyAdmin)
admin.site.register(models.Person, PersonAdmin)
admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.ProductScore, ProductScoreAdmin)
admin.site.register(models.ProductSecurityRole, ProductRoleAdmin)
admin.site.register(models.ProductControl, ProductControlAdmin)
admin.site.register(models.ProductSecurityCapability, ProductSecurityCapabilityAdmin)
admin.site.register(models.SecurityCapability, SecurityCapabilityAdmin)
admin.site.register(models.SecurityCategory, SecurityCategoryAdmin)
admin.site.register(models.SecuritySubCategory, SecuritySubCategoryAdmin)
admin.site.register(models.SecurityRole, SecurityRoleAdmin)
admin.site.register(models.Standard, StandardAdmin)
admin.site.register(models.Status, StatusAdmin)
