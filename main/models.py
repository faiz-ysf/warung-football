import uuid
from django.db import models

class News(models.Model):
    CATEGORY_CHOICES = [
        ('transfer', 'Transfer'),
        ('update', 'Update'),
        ('exclusive', 'Exclusive'),
        ('match', 'Match'),
        ('rumor', 'Rumor'),
        ('analysis', 'Analysis'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    content = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='update')
    thumbnail = models.URLField(blank=True, null=True)
    news_views = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    @property
    def is_news_hot(self):
        return self.news_views > 20

    def increment_views(self):
        self.news_views += 1
        self.save()


class Product(models.Model):
    # NOTE: ini adalah bentuk implementasi saya!
    PRODUCT_OPTIONS: list[tuple[str, str]] = [
        ('shoes', 'Shoes'),
        ('men sportwear', 'Men Sportwear'),
        ('women sportwear', 'Women Sportwear'),
        ('kids sportwear', 'Kids sportwear')
    ];  

    name: str = models.CharField(max_length=255);
    price: int = models.IntegerField(verbose_name="Age");
    descriptions: str = models.TextField();
    thumbnail: str = models.URLField(blank=True, null=True);
    category: str  = models.CharField(max_length=20);
    is_featured: bool = models.BooleanField(default=False); 

