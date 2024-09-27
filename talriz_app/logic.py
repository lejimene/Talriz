from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404

#Testing page, For html and css and how it may look
def test_logic(request):
    return render(request, 'test.html')



#login page 
#Should check for login information 
#Checks database if they exist
#Includes hasing and salting and authentication token 
#and XRSF Token

def login_logic(request):
    return render(request, 'login.html')


#Register page
#Should check if infomration exist
#Provide authentication token and have them signed in
 
def create_logic(request):
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
