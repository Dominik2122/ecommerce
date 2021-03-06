from django.shortcuts import render
from django.views.generic import ListView, DetailView
# Create your views here.
from .models import Product, Category
from carts.models import Cart

class ProductListView(ListView):
    model = Product

class ProductDetailView(DetailView):
    model = Product
    def get_context_data(self,*args,**kwargs):
        context = super(ProductDetailView, self).get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        return context

class GroupListView(ListView):
    model = Category
    
