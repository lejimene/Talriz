# myapp/urls.py
from django.urls import path
from . import views
from django.http import HttpResponse


def not_found(request):
    message = "404 Not Found - Oopies"
    return HttpResponse(message, status=404)

urlpatterns = [
    path('', views.test_page, name="test_page"),  
    path('login/', views.login_page, name="login_page"), 
    path('register/', views.register_page, name="register_page"), 
    path('filters/', views.filters_page, name="filters_page"), 
    path('marketplace/', views.marketplace_page, name="marketplace_page"), 
]






