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

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('items')  # Redirect to the items page upon successful login
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def sign_up_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('items')  # Redirect to the items page upon successful signup
    else:
        form = UserCreationForm()
    return render(request, 'sign_up.html', {'form': form})

from django.contrib.auth.models import User

@login_required
def items(request):
    # Get the user instance from the request
    user_instance = request.user

    # Query items for the user
    user_items = Item.objects.filter(user=user_instance)

    return render(request, 'items.html', {'user_items': user_items})

@csrf_exempt
@login_required
def add_item(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        item_name = data.get('name', '')
        item_price = data.get('price', 0)
        user_instance = request.user
        try:
            # Create the item with the associated user
            Item.objects.create(user=request.user, name=item_name, price=item_price)
            return JsonResponse({'success': True})
        except Exception as e:
            # Handle exceptions, e.g., integrity errors
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False})


@login_required
def calculate_sum(request):
    user_instance = request.user
    user_items = Item.objects.filter(user=user_instance)
    total_cost = sum(item.price for item in user_items)
    return JsonResponse({'total_cost': total_cost})