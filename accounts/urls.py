from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import LoginView, RegisterView


app_name = 'accounts'
urlpatterns = [
    path('login/', LoginView.as_view(), name = 'login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name = 'register'),
]
