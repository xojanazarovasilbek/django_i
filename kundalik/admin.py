from django.contrib import admin
from .models import Category, Card, Transaction
# Register your models here.
admin.site.register(Category)

admin.site.register(Card)

admin.site.register(Transaction)