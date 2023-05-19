from django.db import models

class Category(models.Model):
    symbol = models.CharField(max_length=4, primary_key=True, unique=True, null=False)
    name = models.CharField(max_length=50, null=False)
    description = models.CharField(max_length=255, null=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    is_discount = models.BooleanField(default=False)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    photo = models.ImageField(upload_to='category_photos/', null=True, blank=True)

    def __str__(self):
        return self.symbol + ' - ' + self.name