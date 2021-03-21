from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.forms.models import model_to_dict
from django.views.generic import TemplateView
from django.views.generic.edit import UpdateView
from django.http import JsonResponse



from .models import Cart
from products.models import Product
from orders.models import Order
from billing.models import BillingProfile, Address
from billing.forms import AddressForm
from accounts.forms import LoginForm, GuestForm


# Create your views here.

def cart_home(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)

    return render(request, 'carts/carts_home.html', {"cart": cart_obj})

def cart_update(request):
    if request.is_ajax():
        print(request.POST)
        product_id = request.POST.get('product')
        if product_id is not None:
            try:
                object = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                return redirect('cart:home')
            cart_obj, new_obj = Cart.objects.new_or_get(request)
            if object in cart_obj.products.all():
                cart_obj.products.remove(object)
                added = False
            else:
                cart_obj.products.add(object)
                added = True
        request.session['cart_item']= cart_obj.products.count()
        amount_in_cart = cart_obj.products.count()
        data = {'added': added,
                'counter': amount_in_cart}
        return JsonResponse(data)

    product_id = request.POST.get('product')
    if product_id is not None:
        try:
            object = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return redirect('cart:home')
        cart_obj, new_obj = Cart.objects.new_or_get(request)
        if object in cart_obj.products.all():
            cart_obj.products.remove(object)
            added = False
        else:
            cart_obj.products.add(object)
            added = True
    request.session['cart_item']= cart_obj.products.count()
    amount_in_cart = cart_obj.products.count()

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
        order_obj.billing = billing_profile
        order_obj.save()
    elif 'billing_profile' in request.session.keys():
        if list(request.session.values()):
            billing_profile = BillingProfile.objects.get(pk=list(request.session.values())[2])
            order_obj.billing = billing_profile
            order_obj.save()
        else:
            billing_profile = None
    else:
        guest_form = GuestForm(request.POST)
        billing_profile = None
        if guest_form.is_valid():
            email = guest_form.cleaned_data['email']
            billing_profile = BillingProfile(email=email)
            billing_profile.save()

            request.session['billing_profile'] = billing_profile.id
            order_obj.billing = billing_profile
            order_obj.save()

    if billing_profile:
        if billing_profile.address:
            address = billing_profile.address
        else:
            address_form = AddressForm(request.POST)
            if address_form.is_valid():
                address = address_form.save()
                billing_profile.address = address
                billing_profile.save()
            else:
                address = None
    else:
        address = None

    if request.method == 'POST':
        if 'success' in request.POST:
            order_obj.status = 'paid'
            order_obj.save()
            return redirect('carts:success')

    form = LoginForm()
    guest_form = GuestForm()
    address_form = AddressForm()

    context = {
        "order": order_obj,
        "billing_profile": billing_profile,
        'form': form,
        'guest_form': guest_form,
        'address_form': address_form,
        'address': address
    }
    return render(request, 'carts/checkout.html', context)


class CartSuccess(TemplateView):
    template_name = 'carts/success.html'


class AddressUpdate(UpdateView):
    model = Address
    fields = ['street','city', 'phone']
    template_name = 'carts/address_update.html'
    success_url = reverse_lazy('carts:checkout')
