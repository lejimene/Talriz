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
    path('categories/', views.category_page, name="categories_page"), 
    path('marketplace/', views.marketplace_page, name="marketplace_page"), 
    path('marketplace/item/<int:item_id>/', views.marketplace_searched_item, name="item_detail"),
    path('items/', views.item_listing,name='item_listing'),
    path('sell_page/', views.sell_page, name="sell_page"),
    path('submit_item/', views.submit_item, name="submit_item"),
]






