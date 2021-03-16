from django.shortcuts import render, redirect
from products.models import Product
from .models import Cart
from orders.models import Order
from accounts.forms import LoginForm, GuestForm
from accounts.models import GuestEmail
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
    request.session['cart_item']= cart_obj.products.count()
    return redirect("carts:home")


def checkout_home(request):
    cart_obj, cart_created = Cart.objects.new_or_get(request)
    if cart_created or cart_obj.products.count()==0:
        return redirect('carts:home')
    else:
        order_obj = Order.objects.filter(cart=cart_obj)
        if order_obj.count()==0:
            order_obj =Order(cart=cart_obj)
            order_obj.save()
        else:
            order_obj = order_obj.first()
    user = request.user
    if user.is_authenticated:
        billing_profile = user.billing_profile
    else:
        billing_profile = None
    form = LoginForm()
    guest_form = GuestForm(request.POST)
    if guest_form.is_valid():
        guest_form.save()
        email = guest_form.cleaned_data['email']
        request.session['guest_email_value'] = email
        billing_profile = GuestEmail.objects.filter(email=email).first()
        print(billing_profile)
    context = {
        "order": order_obj,
        "billing_profile": billing_profile,
        'form': form,
        'guest_form': guest_form,
    }
    return render(request, 'carts/checkout.html', context)
