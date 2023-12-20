from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Item
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Item
from django.contrib.auth.decorators import login_required
import json
from django.views.decorators.cache import never_cache
from django.contrib.auth.models import User

def login_view(request):
    ## handle user login form
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            ## validate username and password
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                ## if valid user is found, login and redirect to items page
                login(request, user)
                return redirect('items')
    else:
        ## e.g. if request method is GET, render login page
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def sign_up_view(request):
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            ## if form is valid, save user details and login
            user = form.save()
            login(request, user)
            return redirect('items')
    else:
        ## e.g. if request method is GET, render sign up page
        form = UserCreationForm()
    return render(request, 'sign_up.html', {'form': form})

@login_required
@never_cache
def items(request):
    ## (always assume GET request method)
    user_instance = request.user
    ## get user's items and send data to frontend
    user_items = Item.objects.filter(user=user_instance)
    return render(request, 'items.html', {'user_items': user_items})

@csrf_exempt
@login_required
@never_cache
def add_item(request):
    ## (assume always POST request method)
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        item_name = data.get('name', '')
        item_price = data.get('price', 0)
        try:
            ## Add new item against user's details
            Item.objects.create(user=request.user, name=item_name, price=item_price)
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False})


@login_required
def calculate_sum(request):
    ## simply find user's items and calculate sum, return to front end as "total cost"
    user_instance = request.user
    user_items = Item.objects.filter(user=user_instance)
    total_cost = sum(item.price for item in user_items)
    return JsonResponse({'total_cost': total_cost})