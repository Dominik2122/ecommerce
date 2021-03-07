from django.urls import path, include

from .views import cart_home
app_name = 'carts'
urlpatterns = [
    path('', cart_home, name='home')
]
