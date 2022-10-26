from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login_user, name='login'),
    path('register/', views.register, name='register'),
    path('logout', views.logout_user, name='logout')
]