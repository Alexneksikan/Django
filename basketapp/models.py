from django.conf import settings
from django.db import models

from mainapp.models import Product


class Basket(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='basket')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=0)

    add_datetime = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    @property
    def product_cost(self):
        return self.quantity * self.product.price

    @property
    def total_quantity(self):
        _item = Basket.objects.filter(user=self.user)
        return sum(list(map(lambda x: x.quantity, _item)))

    @property
    def total_cost(self):
        _item = Basket.objects.filter(user=self.user)
        return sum(list(map(lambda x: x.product_cost, _item)))
