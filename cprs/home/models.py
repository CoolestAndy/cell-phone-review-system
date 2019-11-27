from django.contrib.auth.models import User
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Brand(models.Model):
    name = models.CharField(max_length=50)


class Rating(models.Model):
    rating = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )


class Carrier(models.Model):
    CANDIDATES = ['Unlocked', 'AT&T', 'T-Mobile', 'Mint', 'Verizon', 'Sprint', 'MetroPCS', 'Cricket', 'H2O']
    name = models.CharField(max_length=10)


class Item(models.Model):
    asin = models.CharField(primary_key=True, max_length=10)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    carrier = models.ForeignKey(Carrier, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    image = models.URLField()
    ratings = models.ManyToManyField(Rating, through='Review')
    average_rating = models.DecimalField(max_digits=2, decimal_places=1)
    total_reviews = models.IntegerField()
    min_price = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    max_price = models.DecimalField(max_digits=6, decimal_places=2, null=True)


class Review(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.ForeignKey(Rating, on_delete=models.CASCADE)
    date = models.DateField()
    title = models.TextField()
    body = models.TextField()
    helpful_votes = models.IntegerField()
