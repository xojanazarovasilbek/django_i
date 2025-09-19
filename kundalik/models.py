from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="categories")
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Transaction(models.Model):
    TYPE_CHOICES = (
        ('income', 'Kirim'),
        ('expense', 'Chiqim'),
    )
    CURRENCY_CHOICES = (
        ('UZS', 'So‘m'),
        ('USD', 'Dollar'),
        ('CARD', 'Karta'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=4, choices=CURRENCY_CHOICES, default='UZS')
    type = models.CharField(max_length=7, choices=TYPE_CHOICES)
    created_at = models.DateTimeField() 

    def __str__(self):
        return f"{self.type} - {self.amount} {self.currency}"


class Card(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cards")  
    name = models.CharField(max_length=100)
    number = models.CharField(max_length=16, unique=True)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    currency = models.CharField(
        max_length=3,
        choices=[("UZS", "So'm"), ("USD", "Dollar")],
        default="UZS"
    )

    def __str__(self):
        return f"{self.name} ({self.number})"