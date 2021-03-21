from django.urls import path, include

from .views import payment_method_view, payment_method_createview
app_name = 'billing'
urlpatterns = [
    path('', payment_method_view, name='payment-method'),
    path('create/', payment_method_createview, name='payment-method-endpoint'),
]
