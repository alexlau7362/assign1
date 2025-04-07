from django.db import models

# Create your models here.
class Product(models.Model):
    product_code = models.CharField(max_length=10)
    name = models.CharField(max_length=200)
    origin = models.CharField(max_length=100)
    made_in = models.CharField(max_length=100)
    quantity = models.IntegerField()

    def __str__(self):
        return self.name

