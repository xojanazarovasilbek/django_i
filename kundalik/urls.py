from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('transactions/', views.transactions_list, name='transactions'),
    path('transactions/add/', views.add_transaction, name='add_transaction'), 
    path('kirim/', views.Kirim, name='incomes'),
    path('chiqim/', views.Chiqim, name='expenses'),
    path('cards/add/', views.add_card, name='add_card'),
    path('profile/', views.profile, name='profile'),
    path('profile/update/', views.profile_update, name='profile_update'),
]
