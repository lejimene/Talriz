# myapp/urls.py
from django.urls import path
from . import views
from . import logic
from django.http import HttpResponse
from django.conf import settings
from django.conf.urls.static import static
from talriz_app.logic import submit_bid


def not_found(request):
    message = "404 Not Found - Oopies"
    return HttpResponse(message, status=404)

urlpatterns = [ 
    path('', views.login_page, name="login_page"), 
    path('', logic.login_logic, name="login_logic"),
    path('register/', views.register_page, name="register_page"),
    path('register/', logic.create_logic, name='create_logic'), #Logic for when user is registering new user
    path('marketplace/', views.marketplace_page, name="marketplace_page"),
    path('logout/', logic.logout_logic, name="logout_logic"), 
    path('like-item/<int:item_id>/', logic.like_item, name='like_item'),
    path('marketplace/item/<int:item_id>/', views.marketplace_searched_item, name="item_detail"),
    path('buy/<int:item_id>/', views.buy_button_item, name='buy_item'),
    path('items/', views.item_listing,name='item_listing'),
    path('sell_page/', views.sell_page, name="sell_page"),
    path('contact/', views.contact_page, name="contact"),
    path('submit_item/', views.submit_item, name="submit_item"),
    path('submit-messages/', views.submit_messages, name="submit_item"),
    path('login/', views.login_page, name="login_page"),
    path('submit-bid/<int:item_id>/', submit_bid, name='submit_bid'),
]

# This is for serving media files like images for development mode
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)