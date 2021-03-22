from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.http import HttpResponse
# Create your views here.
from orders.models import Order

class SalesView(LoginRequiredMixin, TemplateView):
    template_name = 'analytics/sales.html'

    def dispatch(self, *args, **kwargs):
        user = self.request.user
        if not user.is_staff:
            return HttpResponse('Not allowed', status=401)
        return super(SalesView,self).dispatch(*args, **kwargs)

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        recent_orders = Order.objects.order_by('timestamp')
        print(recent_orders)
        context['recent_orders'] = recent_orders
        return context
