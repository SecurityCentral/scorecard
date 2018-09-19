from django.contrib import admin
from .models import Control, ControlFamily, Product, ProductControl, Standard


class ControlAdmin(admin.ModelAdmin):
    list_display = ('name', 'label', 'family', 'standard')


class ControlFamilyAdmin(admin.ModelAdmin):
    list_display = ('label',)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name',)


class ProductControlAdmin(admin.ModelAdmin):
    list_display = ('status', 'product', 'control')


class StandardAdmin(admin.ModelAdmin):
    list_display = ('name', 'label')


admin.site.register(Control, ControlAdmin)
admin.site.register(ControlFamily, ControlFamilyAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductControl, ProductControlAdmin)
admin.site.register(Standard)
