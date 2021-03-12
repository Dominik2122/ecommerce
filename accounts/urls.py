from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import login_page, register_page


app_name = 'accounts'
urlpatterns = [
    path('login/', login_page, name = 'login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', register_page, name = 'register'),
]
