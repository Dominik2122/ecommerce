from django.urls import path, include

from .views import ProductListView, ProductDetailView, GroupListView

app_name = 'product'
urlpatterns = [
    path('', ProductListView.as_view(), name = 'list'),
    path('group/<int:pk>', GroupListView.as_view(), name = 'group_list' ),
    path('<str:slug>', ProductDetailView.as_view(), name = 'details'),
]
