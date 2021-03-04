from django.urls import path, include

from .views import ProductListView, ProductDetailView

app_name = 'product'
urlpatterns = [
    path('', ProductListView.as_view(), name = 'list'),
    path('<str:slug>', ProductDetailView.as_view(), name = 'details'),
]
