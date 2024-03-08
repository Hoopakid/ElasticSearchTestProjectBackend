from datetime import datetime

from django.db import models
from rest_framework.exceptions import ValidationError


class Products(models.Model):
    product_name = models.CharField(max_length=255)
    product_description = models.TextField()
    product_type = models.CharField(max_length=55)
    product_count = models.IntegerField()
    product_price = models.IntegerField()
    created_at = models.DateTimeField(default=datetime.utcnow)

    def clean(self):
        if self.product_count < 0:
            raise ValidationError("Product count cannot be negative.")

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ['product_name']

    def __str__(self):
        return f'{self.product_name}'
