from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from django.conf import settings


class Manufacturer(models.Model):
    name = models.CharField(max_length=200)


class Language(models.Model):
    name = models.CharField(max_length=20)


class Country(models.Model):
    name = models.CharField(max_length=50)


class Rating(models.Model):
    rating = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )


class Phone(models.Model):
    name = models.CharField(max_length=200)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)
    rating = models.ManyToManyField(Rating)


class Review(models.Model):
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now=True)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    rating = models.ForeignKey(Rating, on_delete=models.CASCADE)
    phone = models.ForeignKey(Phone, on_delete=models.CASCADE)
