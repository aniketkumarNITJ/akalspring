from django.db import models

# Create your models here.


class Product(models.Model):
    product_name = models.TextField(primary_key=True)
    hsnCode = models.TextField(unique=False)
    weight = models.FloatField()

    def __str__(self):
        return self.product_name

