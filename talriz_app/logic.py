import bcrypt
import hashlib
import os
from django.http import HttpResponse
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import Item, ItemImage, Bidder
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.timezone import now
from django.views.decorators.http import require_POST
from rest_framework.authtoken.models import Token
from datetime import timedelta
from django.utils.html import escape
from django.db.models import Prefetch

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
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(email=email)
            user = authenticate(request, username=user.username, password=password)
            if user is not None:
                login(request, user)
                
                # Get or create the token for the user
                token, created = Token.objects.get_or_create(user=user)
                response = JsonResponse({'success': True})
                # Set the token in the response cookie
                response.set_cookie('auth_token', token.key, max_age=3600, httponly=True)
                response['X-Content-Type-Options'] = 'nosniff' # fixes security issue in Part One LO1
                return response
            else:
                return JsonResponse({'error': 'Invalid credentials'}, status=400)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User does not exist'}, status=400)
    return render(request, 'login_page.html')


# Logout logic
# Invalidates tokens and delete cookies
def logout_logic(request):
    # Delete the user's token before logging out
    if request.user.is_authenticated:
        try:
            token = Token.objects.get(user=request.user)
            token.delete()
        except Token.DoesNotExist:
            pass

    # Log the user out
    auth_logout(request)

    # Clear the auth token cookie
    response = redirect('login_page')
    response['X-Content-Type-Options'] = 'nosniff' # fixes security issue in Part One LO1
    response.delete_cookie('auth_token')
    return response

 # Returns a list of reasons why password is not valid
special_chars = ['!','@','#','$','%','^','&','*','(',')','-','+','_','=',]
numbers = ['1','2','3,','4','5','6','7','8','9','0']
def validation(password):
    # Initializing requirements
    upper = False
    lower = False
    special = False
    num = False
    length = False

    # Check for all requirements
    reasons = []
    if len(password) >= 8:
        length = True

    for letter in password:
        if letter.isupper():
            upper = True
        elif letter.islower():
            lower = True
        elif letter in special_chars:
            special = True
        elif letter in numbers:
            num = True

    # Return all requirements failed
    if upper == False:
        reasons.append(" have an uppercase character")
    if lower == False:
        reasons.append(" have a lowercase character")
    if special == False:
        reasons.append(" have a special character")
    if num == False:
        reasons.append(" have a number")
    if length == False:
        reasons.append(" be at least 8 characters long")

    if len(reasons) > 0:
        reasons.insert(0,"Password must...")
    return reasons

#Register page
#Should check if information exist
#Provide authentication token and have them signed in
def create_logic(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')            
        retyped_password = request.POST.get('retyped-password')

        # In order of Registration Page
        # Check if email already exists
        if User.objects.filter(email=email).exists():
            return JsonResponse({'error': "Email already exists"}, status=400)
        
        # Check if username already exists
        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': "Username already exists"}, status=400)
        
        # Check if passwords match
        if password != retyped_password:
            return JsonResponse({'error': 'Passwords do not match'}, status=400)
        
        # Check for password validity
        password_test = validation(password)
        if len(password_test) != 0:
            return JsonResponse({'error': password_test}, status=400)

    
        # Create and log in user if all checks pass
        user = User.objects.create_user(username=username, password=password, email=email)
        login(request, user)

        # Get or create the token for the user
        token, created = Token.objects.get_or_create(user=user)

        response = JsonResponse({'success': True})
        response.set_cookie('auth_token', token.key, max_age=3600, httponly=True)
        response['X-Content-Type-Options'] = 'nosniff' # fixes security issue in Part One LO1

        return response

    return render(request, 'register_page.html')

def like_item(request, item_id):
    if request.method == 'POST' and request.user.is_authenticated:
        item = get_object_or_404(Item, id=item_id)
        if request.user in item.likes.all():
            item.likes.remove(request.user)
            liked = False
        else:
            item.likes.add(request.user)
            liked = True

        response = JsonResponse({'liked': liked, 'likes_count': item.likes.count()})
        response['X-Content-Type-Options'] = 'nosniff' # fixes security issue in Part One LO1
        return response
    return JsonResponse({'error': 'Invalid request'}, status=400)
    

# Market page logic 
# Should be able to dynamically load stuff (Perhaps JS stuff)
# Load info from other users like there items
# We might need to handle How much of it loads cuz imagine
# we load everything with a full database not cool.
def Market_logic(request):
    # Fetch only items with status 'active', along with their related images and likes
    items = (
        Item.objects.prefetch_related(
            Prefetch('images'), 
            Prefetch('likes')
        )
        .filter(status='active')  # Only fetch active items
        .all()
    )
    
    # Paginate the filtered items
    paginator = Paginator(items, 15)
    page_number = escape(request.GET.get('page', 1))

    try:
        page_items = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_items = paginator.get_page(1)
    except EmptyPage:
        page_items = paginator.get_page(paginator.num_pages)

    # Render the template with only active items
    return render(request, 'marketplace_page.html', {'items': page_items})

def Market__focused_item_logic(request,  item_id):
    item = get_object_or_404(Item, id=item_id)
    return render(request, 'marketplace_item',  {'item':item}) 

# sell page logic 
# Should be able to grab input from user and store in database
# Load info from other users
def Sell_logic(request):
    return render(request, 'sell_page.html')

def buy_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    
    # Ensure the buyer is not the seller
    if request.user == item.seller:
        return JsonResponse({'error': 'You cannot buy your own item.'}, status=403)

    # Update the item's status to 'sold'
    if item.status == 'active':
        item.status = 'sold'
        item.save()
        return JsonResponse({'message': 'Item purchased successfully!'})
    else:
        return JsonResponse({'error': 'Item is not available for purchase.'}, status=400)

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Bid submitting functions
@csrf_exempt
def submit_bid(request, item_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            new_bid = data.get("bid")

            # Fetch the item
            item = Item.objects.get(id=item_id)

            if new_bid > item.bid_amount:
                item.bid_amount = new_bid
                item.save()
                return JsonResponse({"new_bid": item.bid_amount}, status=200)
            else:
                return JsonResponse({"error": "Bid must be higher than the current bid."}, status=400)

        except Item.DoesNotExist:
            return JsonResponse({"error": "Item not found."}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method."}, status=405)


#Whats the point of this code actually literally doesnt effect anything if
#user wants to seel an item
# # Handle listing a new item to the database that user posted
# def list_item(request):
#     if request.method == 'POST':
#         #Get data from the form
#         name = escape(request.POST.get('item_name'))
#         description = escape(request.POST.get('item_description'))
#         price = request.POST.get('item_price')
#         image = request.POST.get('item_image')
        
#         # Handle auction-specific fields
#         is_auction = request.POST.get('is_auction', False)
#         bid_amount = request.POST.get('bid_amount', None)
#         buy_out_price = request.POST.get('buy_out', None)
#         auction_end_date = request.POST.get('auction_end_date', None)
#         auction_end_time = request.POST.get('auction_end_time', None)

#         #Combine auction end date and auction end time
#         if auction_end_date and auction_end_time:
#             auction_end_datetime = f"{auction_end_date} {auction_end_time}"
#         else:
#             auction_end_datetime = None

#         seller = request.user if request.user.is_authenticated else User.objects.get(id=1)
#         new_item = Item(
#             seller = seller,
#             name= name,
#             image= image,
#             description = description,
#             price=price if not is_auction else None,
#             starting_bid=bid_amount if is_auction else None,
#             buy_out_price=buy_out_price if is_auction else None,
#             auction_end_date=auction_end_datetime if is_auction else None
#         )
#         new_item.save()

#         #Save category BUT CATEGORY DOESNT WORK AS OF NOW
#         # category_instance

#         #redirect page if item is submitted
#         return redirect() 
    
#     return render(request, 'sell_page.html')