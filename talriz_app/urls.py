# myapp/urls.py
from django.urls import path
from . import views
from . import logic
from django.http import HttpResponse


def not_found(request):
    message = "404 Not Found - Oopies"
    return HttpResponse(message, status=404)

urlpatterns = [ 
    path('', views.login_page, name="login_page"), 
    path('', logic.login_logic, name="login_logic"),
    path('register/', views.register_page, name="register_page"),
    path('register/', logic.create_logic, name='create_logic'), #Logic for when user is registering new user
    path('categories/', views.category_page, name="categories_page"), #Might be worth cutting this out since its not neccesary.
    path('marketplace/', views.marketplace_page, name="marketplace_page"),
    path('logout/', logic.logout_logic, name="logout_logic"), 
    path('like-item/<int:item_id>/', logic.like_item, name='like_item'),
    path('marketplace/item/<int:item_id>/', views.marketplace_searched_item, name="item_detail"),
    path('items/', views.item_listing,name='item_listing'),
    path('sell_page/', views.sell_page, name="sell_page"),
    path('submit_item/', views.submit_item, name="submit_item"),
    path('testing/', views.test_page, name="test_page"),  #This is to test how our pages handle frontend.
    path('login/', views.login_page, name="login_page"),
]






