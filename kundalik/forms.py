from django import forms
from .models import Transaction
from .models import Category, Card
from django.contrib.auth.models import User


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name"]


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['category', 'amount', 'currency', 'type','created_at']
        widgets = {
            'created_at': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local',  
                    'class': 'form-control'
                }
            )
        }
        
class CardForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = ['name', 'balance']

class ProfilForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }