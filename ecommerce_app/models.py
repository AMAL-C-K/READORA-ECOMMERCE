from django.db import models
from django.utils.text import slugify
from django.urls import reverse

#model for Book Categories

class Genre(models.Model):
    genre = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.genre
    
    def get_genre_url(self):
        return reverse('genre', args=[self.slug])
    
#model for Book

class Book(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    slug = models.SlugField(unique=True,blank=True)
    author  = models.CharField(max_length=150)
    price = models.IntegerField()
    stock = models.PositiveIntegerField()
    image = models.ImageField(upload_to='book_images/',null=True,blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return self.title

    def get_book_url(self):
        return reverse('book',args=[self.genre.slug, self.slug])