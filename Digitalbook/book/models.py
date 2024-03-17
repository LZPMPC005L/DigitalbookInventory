from audioop import reverse
from datetime import date

#from django.contrib.gis.tests.relatedapp.models import Book
from django.db import models
from django.http import JsonResponse
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.
class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

class Book(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    published_date = models.DateField(default=date.today)
    #author = models.ManyToManyField(User, related_name='author_book')
    author = models.ManyToManyField(Author, related_name='books')
    price = models.DecimalField(max_digits=5, decimal_places=2)
    subject = models.CharField(max_length=100)
