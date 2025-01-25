from django.db import models
from django.conf import settings
from django.db.models import Avg
import uuid

class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    label = models.CharField(max_length=50)
    brand = models.CharField(max_length=100)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    ingredients = models.TextField()
    combination = models.BooleanField(default=False)
    dry = models.BooleanField(default=False)
    normal = models.BooleanField(default=False)
    oily = models.BooleanField(default=False)
    sensitive = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.brand} - {self.name}"

    def average_rating(self):
        avg_rating = self.ratings.aggregate(Avg('rating'))['rating__avg']
        return round(avg_rating, 1) if avg_rating else 0

    def total_ratings(self):
        return self.ratings.count()

    def recent_comments(self):
        return self.comments.order_by('-timestamp')[:3]

from django.db import models
from django.conf import settings
import uuid

class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    label = models.CharField(max_length=50)
    brand = models.CharField(max_length=100)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    ingredients = models.TextField()
    combination = models.BooleanField(default=False)
    dry = models.BooleanField(default=False)
    normal = models.BooleanField(default=False)
    oily = models.BooleanField(default=False)
    sensitive = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.brand} - {self.name}"

    def average_rating(self):
        avg_rating = self.ratings.aggregate(models.Avg('rating'))['rating__avg']
        return round(avg_rating, 1) if avg_rating else 0

    def total_ratings(self):
        return self.ratings.count()

    def recent_comments(self):
        return self.ratings.order_by('-timestamp')[:3]  # Get comments via ratings


class RatingComment(models.Model):  
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]
    
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, related_name="ratings", on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField()  # Merged comment with rating
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} rated {self.rating} ⭐ - {self.comment[:30]}..."

class Wishlist(models.Model):
    """Wishlist untuk menyimpan produk favorit user"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="wishlist")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="wishlist_items")
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "product")  # Mencegah user memasukkan produk yang sama lebih dari sekali

    def __str__(self):
        return f"{self.user.username} ❤️ {self.product.name}"