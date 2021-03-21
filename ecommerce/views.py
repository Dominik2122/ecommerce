from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.urls import reverse
from django.http import JsonResponse
from django.core import serializers
from django.forms.models import model_to_dict


from carts.models import Cart
from products.models import Product

import random


class HomePage(TemplateView):
    template_name = 'index.html'
    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            products = Product.objects.all()
            products = list(products)
            random.shuffle(products)
            d = []
            d = []
            for product in products[:6]:
                pro = model_to_dict(product, fields=('title', 'price', 'active', 'slug'))
                if product.image:
                    pro['url'] =  product.image.url
                else:
                    pro['url'] = '/media/products/Profile-NotAvailable-300x300.png'
                d.append(pro)
            return JsonResponse({'products': d})
        return super().get(request, *args, **kwargs)
