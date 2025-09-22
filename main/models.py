import uuid
from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    PRODUCT_OPTIONS = [
        ('shoes', 'Shoes'),
        ('men sportwear', 'Men Sportwear'),
        ('women sportwear', 'Women Sportwear'),
        ('kids sportwear', 'Kids Sportwear'),
        ('accessories', 'Accessories'),
        ('equipment', 'Sports Equipment'),
        ('bags', 'Bags & Backpacks'),
        ('outerwear', 'Jackets & Hoodies'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=255)
    price = models.IntegerField(verbose_name="Price")
    descriptions = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    item_views = models.PositiveIntegerField(default=0)
    thumbnail = models.URLField(blank=True, null=True)
    category = models.CharField(max_length=50, choices=PRODUCT_OPTIONS)
    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    @property
    def is_product_trending(self):
        return self.item_views > 20

    def increment_views(self):
        self.item_views += 1
        self.save()

    
    

