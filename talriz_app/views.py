from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from .import logic


# Views is basically like Router but not with POST , GET , DELETE

def login_page(request):
    response = logic.login_logic(request)
    return response

def register_page(request):
    response = logic.login_logic(request)
    return response

def filters_page(request):
    response = logic.login_logic(request)
    return response

def marketplace_page(request):
    response = logic.login_logic(request)
    return response
