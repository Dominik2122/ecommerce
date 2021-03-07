from django.shortcuts import render
from .models import Cart
# Create your views here.




def cart_create(user=None):
    cart_obj = Cart.objects.crate(user = None)
    return cart_obj



def cart_home(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    products = cart_obj.products.all()
    total = 0
    for item in products:
        total = item.price
    cart_obj.total = total
    cart_obj.save()

    return render(request, 'carts/carts_home.html', {})
