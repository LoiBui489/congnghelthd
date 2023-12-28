from django.contrib import admin

from .models import Category, Product, Menu, MyMenuProduct


class MenuAdminInline(admin.TabularInline):
    model = MyMenuProduct
    extra = 1


class MenuAdmin(admin.ModelAdmin):
    inlines = (MenuAdminInline,)


admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Menu, MenuAdmin)
