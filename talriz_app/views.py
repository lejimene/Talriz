# myapp/views.py
from django.shortcuts import render
from django.http import HttpResponse
from . import logic
from django.http import HttpResponse
from . import logic

def my_view(request):
    method = request.method         
    path = request.path            
    headers = request.headers       
    body = request.body            
    cookies = request.COOKIES       

    # Process the request as needed
    return HttpResponse("Request.")

def test_page(request):
    response = logic.test_logic(request)
    return response

def login_page(request):
    response = logic.login_logic(request)
    return response

def register_page(request):
    response = logic.register_logic(request)
    return response

def filters_page(request):
    response = logic.filters_logic(request)
    return response

def marketplace_page(request):
    response = logic.marketplace_logic(request)
    return response

