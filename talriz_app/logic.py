import bcrypt
import hashlib
import os
from django.http import HttpResponse
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
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
    return render(request,'categories.html')

# Market page logic 
# Should be able to dynamically load stuff (Perhaps JS stuff)
# Load info from other users
def Market_logic(request):
    return render(request, 'marketplace.html')


# Logout logic
# Invalidates tokens and delete cookies
def logout_logic(request):
    if 'auth_token' in request.COOKIES:
        token = request.COOKIES['auth_token']
        try:
            user = User.objects.get(auth_token=hashlib.sha256(token.encode('utf-8')).hexdigest())
            user.auth_token = None
            user.save()
        except User.DoesNotExist:
            pass

    response = redirect('login_page')
    response.delete_cookie('auth_token')
    return response