from django.urls import path, include
from .views import SalesView

app_name = 'analytics'
urlpatterns = [
    path('', SalesView.as_view(), name='sales'),

]
