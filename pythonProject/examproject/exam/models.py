from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import CASCADE


class BaseModel(models.Model):
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class User(AbstractUser):
    avatar = models.ImageField(upload_to='uploads/%Y/%m')


class Category(models.Model):
    name = models.CharField(null=False, unique=True, max_length=100)

    def __str__(self):
        return self.name


class Product(BaseModel):
    name = models.CharField(null=False, max_length=100)
    description = models.TextField(null=True, blank=True)

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

    def __str__(self):
        return self.name


class MyMenuProduct(models.Model):
    menu = models.ForeignKey(Menu, on_delete=CASCADE)
    product = models.ForeignKey(Product, on_delete=CASCADE)
    product_sell_from_time = models.DateTimeField(null=True)
    product_sell_to_time = models.DateTimeField(null=True)
    in_stock = models.BooleanField(default=True)
