from django.urls import path
from .views import login_view, sign_up_view, items, add_item, calculate_sum

urlpatterns = [
    path('login/', login_view, name='login'),
    path('sign_up/', sign_up_view, name='signup'),
    path('items/', items, name='items'),
    path('add_item/', add_item, name='add_item'), 
    path('calculate_sum/', calculate_sum, name='calculate_sum'),
]