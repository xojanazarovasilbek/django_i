from django.urls import path
from .views import register_view, login_view,logout_view,change_pass_view,reset_pass,reset_pass2

urlpatterns = [
    path('', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('chang-pas/', change_pass_view, name='change-pass'),
    path('reset/', reset_pass, name='reset'),
    path('reset2/', reset_pass2, name='reset2')
]
