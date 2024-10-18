import bcrypt
import hashlib
import os
from django.http import HttpResponse
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import Item, Category, ItemImage
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.timezone import now
from datetime import timedelta

#Testing page, For html and css and how it may look
#replace the test.html with actual html page
def test_logic(request):
    return render(request, 'marketplace_page.html')


# Generates a random authentication token
def generate_token():
    return hashlib.sha256(os.urandom(32)).hexdigest()



#login page 
#Should check for login information 
#Checks database if they exist
#Includes hasing and salting and authentication token 
#and XRSF Token

def login_logic(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
            if user.check_password(password.encode('utf-8'), user.password.encode('utf-8')):
                token = generate_token()
                user.auth_token = hashlib.sha256(token.encode('utf-8')).hexdigest()
                user.save()

                response = JsonResponse({'message': 'Login successful'})
                response.set_cookie('auth_token', token, max_age=3600, httponly=True)
                return response
            else:
                return JsonResponse({'error': 'Invalid password'}, status=400)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=400)
    return render(request, 'login_page.html')



#Register page
#Should check if infomration exist
#Provide authentication token and have them signed in
 
def create_logic(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': 'Username already exists'}, status=400)

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        User.objects.create(username=username, password=hashed_password.decode('utf-8'))

        return JsonResponse({'message': 'User registered successfully'}, status=200)

    return render(request, 'register_page.html')


#category Page
#Given set categories could be from user or from us ADMINS
def category_logic(request):
    categories = Category.objects.all()  # Get all categories
    return render(request, 'filters_page.html', {'categories': categories})

# Market page logic 
# Should be able to dynamically load stuff (Perhaps JS stuff)
# Load info from other users like there items
# We might need to handle How much of it loads cuz imagine
# we load everything with a full database not cool.
def Market_logic(request):
    items = Item.objects.prefetch_related('images', 'likes').all()  # Fetch items with related images and likes,
    #This items fetches everything we should be worried about it a litle
    paginator = Paginator(items, 15)
    page_number = request.GET.get('page',1)

    #handling paginator which is what keeps page laoding for more\
    #This means if we create a filters so the user can't
    try:
        page_items = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_items = paginator.get_page(1)
    except EmptyPage:
        page_items = paginator.get_page(paginator.num_pages)

    return render(request, 'marketplace_page.html', {'items': page_items})

def Market__focused_item_logic(request,  item_id):
    item = get_object_or_404(Item, id=item_id)
    return render(request, 'marketplace_item',  {'item':item}) 

# sell page logic 
# Should be able to grab input from user and store in database
# Load info from other users
def Sell_logic(request):
    return render(request, 'sell_page.html')

def submit_item(request):
    if request.method == 'POST':
        #Get data from the form
        name = request.POST.get('item_name')
        description = request.POST.get('item_description')
        price = request.POST.get('item_price')
        category = request.POST.get('item_category')
        
        # Handle auction-specific fields
        is_auction = request.POST.get('is_auction', False)
        starting_bid = request.POST.get('starting_bid', None)
        buy_out_price = request.POST.get('buy_out', None)
        auction_end_date = request.POST.get('auction_end_date', None)
        auction_end_time = request.POST.get('auction_end_time', None)

        #Combine auction end date and auction end time
        if auction_end_date and auction_end_date:
            auction_end_datetime = f"{auction_end_date} {auction_end_date}"
        else:
            auction_end_datetime = None

        seller = User.objects.get(id=1)
        new_item = Item(
            seller = seller,
            name= name,
            description = description,
            price=price if not is_auction else None,
            starting_bid=starting_bid if is_auction else None,
            buy_out_price=buy_out_price if is_auction else None,
            auction_end_date=auction_end_datetime if is_auction else None
        )
        new_item.save()

        #Save category BUT CATEGORY DOESNT WORK AS OF NOW
        # category_instance

        #redirect page if item is submitted
        return redirect() 
    
    return render(request, 'sell_page.html')