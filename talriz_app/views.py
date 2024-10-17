# myapp/views.py
from django.shortcuts import render
from django.http import HttpResponse
from . import logic
from django.http import HttpResponse
from . import logic
from django.contrib.auth.decorators import login_required


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
    if request.method == 'POST':
        response = logic.login_logic(request)
        return response
    return render(request, 'login_page.html')


def register_page(request):
    if request.method == 'POST':
        response = logic.create_logic(request)
        return response
    return render(request, 'register_page.html')

## is this catagory logic
def category_page(request):
    if request.method == "POST":
        response = logic.category_logic(request)
        return response
    response = logic.category_logic(request)
    return response


#This is the page that will load all items with no specific look into it
def marketplace_page(request):
    if request.method == 'POST':
        response = logic.Market_logic(request)
        return response
    response = logic.Market_logic(request)
    return response


#This is the page tht will handle loading a specific item and getting the details of it
def marketplace_searched_item(request, item_id):
    if request.method == 'POST':
        response = logic.Market__focused_item_logic(request, item_id)
        return response
    return render(request, 'marketplace_page.html')


# Handle listing a new item to the database that user posted
def item_listing(request):
    if request.method == 'POST':
        response = logic.submit_item(request)
        return response 
    
