from django.contrib import admin

from .models import Category, Product, Menu, MyMenuProduct, Department, MyMenuDepartment, MyOrderProduct, Order


class MenuAdminInline(admin.TabularInline):
    model = MyMenuProduct
    extra = 1


class DepartmentAdminInline(admin.TabularInline):
    model = MyMenuDepartment
    extra = 1


class OrderAdminInline(admin.TabularInline):
    model = MyOrderProduct
    extra = 1


class MenuAdmin(admin.ModelAdmin):
    inlines = (MenuAdminInline, DepartmentAdminInline)


class DepartmentAdmin(admin.ModelAdmin):
    inlines = (DepartmentAdminInline,)


class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderAdminInline,)


admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Menu, MenuAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(MyMenuDepartment)
admin.site.register(MyMenuProduct)
admin.site.register(MyOrderProduct)
