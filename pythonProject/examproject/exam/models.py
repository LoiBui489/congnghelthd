from cloudinary.models import CloudinaryField
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import CASCADE, SET_NULL


class BaseModel(models.Model):
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class InterationModel(BaseModel):
    user = models.ForeignKey('User', on_delete=CASCADE, null=False)
    department = models.ForeignKey('Department', on_delete=CASCADE)

    class Meta:
        abstract = True


class User(AbstractUser):
    avatar = CloudinaryField('avatar', null=True)
    role = models.CharField(max_length=10, default='ROLE_USER')
    address = models.TextField(null=False, blank=False)


class Category(BaseModel):
    name = models.CharField(null=False, unique=True, max_length=100)

    def __str__(self):
        return self.name


class Product(BaseModel):
    name = models.CharField(null=False, max_length=100)
    description = models.TextField(null=True, blank=True)
    price = models.BigIntegerField(null=False)

    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products')

    class Meta:
        unique_together = ('name', 'category')

    def __str__(self):
        return self.name


class Menu(BaseModel):
    name = models.CharField(null=False, max_length=100)
    description = models.TextField(null=True, blank=True)
    menu_sell_from_time = models.DateTimeField(null=True)
    menu_sell_to_time = models.DateTimeField(null=True)

    products = models.ManyToManyField('Product', related_name='menus', through='MyMenuProduct')
    departments = models.ManyToManyField('Department', related_name='menus', through='MyMenuDepartment')

    def __str__(self):
        return self.name


class Department(BaseModel):
    name = models.CharField(max_length=100, blank=False, null=False)
    address = models.CharField(max_length=200, blank=False, null=False)
    phone_number = models.CharField(max_length=11, blank=False, null=False)
    map_location = models.TextField(null=False, blank=False)
    shipping_fee = models.IntegerField(null=False, default=0)

    manager = models.ForeignKey('User', related_name='departments', on_delete=SET_NULL, null=True)

    def __str__(self):
        return self.name


class Order(BaseModel):
    status = models.CharField(max_length=10, null=False, blank=False)
    shipping_address = models.CharField(max_length=200, blank=False, null=False)
    shipping_fee = models.BigIntegerField(null=False, default=0)
    total_fee = models.BigIntegerField(null=False)
    payed = models.BigIntegerField(null=True, default=0)
    pay_by = models.CharField(max_length=10, null=False)

    department = models.ForeignKey(Department, on_delete=CASCADE, null=False)
    ordered_user = models.ForeignKey(User, on_delete=CASCADE, null=False)
    products = models.ManyToManyField('Product', related_name='orders', through='MyOrderProduct')


class Follow(InterationModel):
    following = models.BooleanField(default=True)


class Comment(InterationModel):
    content = models.CharField(max_length=200, blank=True)
    product = models.ForeignKey('Product', on_delete=SET_NULL, null=True)


class Rating(InterationModel):
    point = models.SmallIntegerField(null=True, validators=[MinValueValidator(0), MaxValueValidator(10)])
    product = models.ForeignKey('Product', on_delete=SET_NULL, null=True)


class MyMenuProduct(BaseModel):
    menu = models.ForeignKey(Menu, on_delete=SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=SET_NULL, null=True)
    product_sell_from_time = models.DateTimeField(null=True)
    product_sell_to_time = models.DateTimeField(null=True)
    in_stock = models.BooleanField(default=True)


class MyMenuDepartment(BaseModel):
    menu = models.ForeignKey(Menu, on_delete=SET_NULL, null=True)
    department = models.ForeignKey(Department, on_delete=SET_NULL, null=True)
    description = models.TextField(null=True, blank=True)
    selling_time = models.CharField(max_length=10, blank=True, default='')


class MyOrderProduct(BaseModel):
    order = models.ForeignKey(Order, on_delete=CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=SET_NULL, null=True)
    product_price = models.BigIntegerField(null=False)
    quantity = models.SmallIntegerField(null=False, default=1)
    user_request = models.TextField(null=True, blank=True)
