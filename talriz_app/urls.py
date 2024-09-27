from django.urls import path
from django.urls import include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.test_page,name="test_page"),
    path('',views.login_page,name="login_page")
]
