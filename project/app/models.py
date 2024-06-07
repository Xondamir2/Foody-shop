from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField()
    price = models.DecimalField(max_digits=7, decimal_places=0)
    quantity = models.IntegerField(default=0)
    discount = models.FloatField(null=True, blank=True)
    image = models.ImageField(upload_to='products/', verbose_name="Rasmi")

    def __str__(self):
        return self.name


class News(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='products/', verbose_name="Rasmi")
    description = models.TextField()
    view = models.IntegerField(default=0)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    first_name = models.CharField(max_length=50, null=True, default='')
    last_name = models.CharField(max_length=50, null=True, default='')


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    created = models.DateTimeField(auto_now_add=True)
    is_activ = models.BooleanField(default=True)

    @property
    def get_cart_total_price(self):
        order_products = self.orderproduct_set.all()
        total_price = sum([product.get_cart_price for product in order_products])
        return total_price

    @property
    def get_cart_total_quantity(self):
        order_products = self.orderproduct_set.all()
        total_quantity = sum([product.quantity for product in order_products])
        return total_quantity



class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0)
    added = models.DateTimeField(auto_now_add=True)

    @property
    def get_cart_price(self):
        total_price = self.quantity * self.product.price
        return total_price


