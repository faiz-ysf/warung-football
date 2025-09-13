import uuid
from django.db import models


class Product(models.Model):
    # NOTE: ini adalah bentuk implementasi saya!
    PRODUCT_OPTIONS: list[tuple[str, str]] = [
        ('shoes', 'Shoes'),
        ('men sportwear', 'Men Sportwear'),
        ('women sportwear', 'Women Sportwear'),
        ('kids sportwear', 'Kids Sportwear'),
        ('accessories', 'Accessories'),
        ('equipment', 'Sports Equipment'),
        ('bags', 'Bags & Backpacks'),
        ('outerwear', 'Jackets & Hoodies'),
    ]

    id: str = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name: str = models.CharField(max_length=255);
    price: int = models.IntegerField(verbose_name="Price");
    descriptions: str = models.TextField();

    date: str = models.DateTimeField(auto_now_add=True);
    item_views: int = models.PositiveIntegerField(default=0);
    thumbnail: str = models.URLField(blank=True, null=True);
    category: str  = models.CharField(max_length=50, choices=PRODUCT_OPTIONS);
    is_featured: bool = models.BooleanField(default=False); 

    def __str__(self):
        return self.name


    @property
    def is_product_trending(self):
        return self.item_views > 20
    
    def increment_views(self):
        self.item_views += 1
        self.save()

    
    

