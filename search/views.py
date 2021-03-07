from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, DetailView
# Create your views here.
from products.models import Product
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.http import JsonResponse
from django.core import serializers
from django.forms.models import model_to_dict


class SearchView(ListView):
    model = Product
    template_name = 'products/product_list.html'
    def get(self,*args, **kwargs):
        request = self.request
        search = request.GET.get('search')
        query = search
        if request.is_ajax():
            search = request.GET.get('search')
            query = search
        if query != None:
            products = Product.objects.filter(title__icontains = query)
            d = []
            for product in list(products)[:12]:
                pro = model_to_dict(product, fields=('title', 'price', 'active', 'slug'))
                if product.image:
                    pro['url'] =  product.image.url
                else:
                    pro['url'] = '/media/products/Profile-NotAvailable-300x300.png'
                d.append(pro)
            return JsonResponse({'products': d})
        else:
            return HttpResponseRedirect(reverse('index'))

        return super().get(request, *args, **kwargs)
