# myapp/views.py
import json
import os
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from . import logic
from django.contrib.auth.decorators import login_required
from .forms import ItemForm, ItemImageForm
from .models import Item, ItemImage, Message, Conversation
from django.contrib import messages
from datetime import datetime
from django.template.loader import render_to_string
from django.db.models import Q
from django.contrib.auth.models import User

from talriz_app import models


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
    
@login_required
def contact_page(request, conversation_id=None):
    # A conversation id is passed in, meaning a conversation is selected
    if conversation_id:
        try:
            conversation = Conversation.objects.get(id=conversation_id)
        except Conversation.DoesNotExist:
            return redirect('contact_page')
        
        messages = Message.objects.filter(conversation=conversation).order_by('timestamp')
        conversations = Conversation.objects.filter(
            Q(user1=request.user) | Q(user2=request.user)
        )
        if request.user == conversation.user1:
            currently_messaging = conversation.user2.username
        else:
            currently_messaging = conversation.user1.username

        # New message is being sent
        if request.method == 'POST':
            message = request.POST.get('message')
            if message:
                Message.objects.create(
                    buyer=conversation.user1.username, 
                    seller=conversation.user2.username, 
                    data=message, 
                    conversation=conversation
                    )
                return redirect('contact_conversation_page', conversation_id=conversation_id)

        return render(request, 'contact_page.html', {'conversation_id': conversation.id, 'messages': messages, 'conversations': conversations, 'currently_messaging': currently_messaging})

    # No conversation id, meaning no conversation is selected.
    conversations = Conversation.objects.filter(user1=request.user) | Conversation.objects.filter(user2=request.user)
    seller = request.POST.get("seller_name", None)

    if seller:
        seller_user = User.objects.get(username=seller)
        buyer_user = request.user  # The logged-in user is the buyer

        conversation = Conversation.objects.filter(
            (Q(user1=buyer_user) & Q(user2=seller_user)) | 
            (Q(user1=seller_user) & Q(user2=buyer_user))
        ).first()

        if not conversation:
            # If no conversation exists, create a new one
            conversation = Conversation.objects.create(user1=buyer_user, user2=seller_user)

        # Redirect to the existing or newly created conversation
        return redirect('contact_conversation_page', conversation_id=conversation.id)

    return render(request, 'contact_page.html', {'conversations': conversations})


@login_required
def submit_messages(request):
    jsonString = json.loads(request.body)
    print(jsonString)
    buyer = jsonString["buyer"]
    seller = jsonString["seller"]
    data = jsonString["message"]
    current_id = jsonString["id"]
    try :
        message = Message.objects.create(buyer=buyer, seller=seller, data=data, id=current_id,)
        message.save()
    except IntegrityError :
        print("Caught dupe message - Oop")

    response = redirect('contact')
    return response

@login_required
def submit_likes(request):
    jsonString = json.loads(request.body)
    print(jsonString)
    Count = jsonString["Likes"]
    item_id = jsonString["item_id"]

    try :
        item = Item.objects.get(id=item_id)
        item.likes.add(Count)
        item.save()
    except Item.DoesNotExist :
        pass

    response = redirect('marketplace_page')
    return response

