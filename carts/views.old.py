from django.shortcuts import render

from .models import Cart

def cart_create(user=None):
	cart_obj = Cart.objects.create(user=None)  
	print('New Cart created')
	return cart_obj

def cart_home(request):
	cart_obj = Cart.objects.new_or_get(request)

	return render(request, "carts/home.html", {})



