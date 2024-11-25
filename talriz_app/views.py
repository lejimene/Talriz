# myapp/views.py
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from . import logic
from django.contrib.auth.decorators import login_required
from .forms import ItemForm, ItemImageForm
from .models import ItemImage
from django.contrib import messages
from datetime import datetime

@login_required
def my_view(request):
    method = request.method         
    path = request.path            
    headers = request.headers       
    body = request.body            
    cookies = request.COOKIES       

    # Process the request as needed
    return HttpResponse("Request.")

@login_required
def test_page(request):
    response = logic.test_logic(request)
    return response

def login_page(request):
    if request.user.is_authenticated and request.method == 'GET':
        response = redirect('marketplace_page')
        return response
    if request.method == 'POST':
        response = logic.login_logic(request)
        return response
    return render(request, 'login_page.html')

@login_required
def sell_page(request):
    return render(request, 'sell_page.html')
    
@login_required
def submit_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        form.instance.seller = request.user
        
        if form.is_valid():
            item = form.save(commit=False)
            
            # Combine auction_end_date and auction_end_time in the view
            if item.is_auction:
                auction_end_date = request.POST.get('auction_end_date')
                auction_end_time = request.POST.get('auction_end_time')
                
                if auction_end_date and auction_end_time:
                    # Combine the date and time into a datetime object
                    auction_end_str = f"{auction_end_date} {auction_end_time}"
                    item.auction_end_datetime = datetime.strptime(auction_end_str, "%Y-%m-%d %H:%M")
                
            item.save()

            # Handle images
            images = request.FILES.getlist('image')
            for image in images[:8]:
                ItemImage.objects.create(item=item, image=image)

            print("Item saved successfully")
            return HttpResponseRedirect('/marketplace/')
        else:
            print("Form errors:", form.errors)
            return HttpResponse("Form is not valid")
    else:
        form = ItemForm()

    return render(request, 'submit_item.html', {'form': form})


def register_page(request):
    if request.method == 'POST':
        response = logic.create_logic(request)
        return response
    return render(request, 'register_page.html')


#This is the page that will load all items with no specific look into it
@login_required
def marketplace_page(request):
    if request.method == 'POST':
        print("Posted")
        response = logic.Market_logic(request)
        return response
    response = logic.Market_logic(request)
    return response

@login_required
def buy_button_item(request,item_id):
    response = logic.buy_item(request,item_id)
    return response
    

#This is the page tht will handle loading a specific item and getting the details of it
@login_required
def marketplace_searched_item(request, item_id):
    if request.method == 'POST':
        response = logic.Market__focused_item_logic(request, item_id)
        return response
    return render(request, 'marketplace_page.html')


# Handle listing a new item to the database that user posted
@login_required
def item_listing(request):
    if request.method == 'POST':
        response = logic.list_item(request)
        return response 
    
