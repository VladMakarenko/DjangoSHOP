from django.contrib.auth.models import AbstractUser
from django.db import models


class MyUser(AbstractUser):
    wallet = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)


class Product(models.Model):
    product_name = models.CharField(max_length=100)
    image = models.URLField()
    description = models.TextField()
    price = models.DecimalField(max_digits=7, decimal_places=2)
    quantity = models.PositiveSmallIntegerField()

    class Meta:
        ordering = ['product_name']
        verbose_name = 'product'
        verbose_name_plural = 'products'

    def __str__(self):
        return self.product_name


class Purchase(models.Model):
    customer = models.ForeignKey(MyUser, related_name='purchases', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']
        verbose_name = 'purchase'
        verbose_name_plural = 'purchases'

    def __str__(self):
        return f'{self.product}'

    def total_price(self):
        return self.quantity * self.product.price


class Return(models.Model):
    purchase = models.OneToOneField(Purchase, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f'{self.purchase}'
