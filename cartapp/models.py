from django.db import models
from django.contrib.auth.models import User
from ecommerce_app.models import Book
import datetime

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveBigIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    def total(self):
        return self.book.price*self.quantity
    

#checkout

class Checkout(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)  
    amount = models.CharField(max_length=150)
    book = models.CharField(max_length=255, null=True)
    payment_id = models.CharField(max_length=150)
    paid = models.BooleanField(default=False)
    ordered_date = models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        return self.cart.book.title
