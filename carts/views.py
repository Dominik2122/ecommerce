from django.shortcuts import render, redirect
from products.models import Product
from .models import Cart
# Create your views here.

def cart_home(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)

    return render(request, 'carts/carts_home.html', {"cart": cart_obj})

def cart_update(request):
    product_id = request.POST.get('product')
    if product_id is not None:
        try:
            object = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return redirect('cart:home')
        cart_obj, new_obj = Cart.objects.new_or_get(request)
        if object in cart_obj.products.all():
            cart_obj.products.remove(object)
        else:
            cart_obj.products.add(object)
    return redirect("carts:home")
