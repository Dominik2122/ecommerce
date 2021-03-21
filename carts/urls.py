from django.urls import path, include

from .views import cart_home, cart_update, checkout_home, CartSuccess, AddressUpdate
app_name = 'carts'
urlpatterns = [
    path('', cart_home, name='home'),
    path('update/', cart_update, name='update'),
    path('checkout/', checkout_home, name='checkout'),
    path('success/', CartSuccess.as_view(), name = 'success'),
    path('address-update/<int:pk>/',  AddressUpdate.as_view(), name = 'address_update')
]
