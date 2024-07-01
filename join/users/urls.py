from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    activate,
    homepage,
    CustomLoginView,
    RegisterView,
    profile,
    CustomLogoutView,
    logout_success
)

app_name = 'users'

urlpatterns = [
    path('', homepage, name='home'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('profile/', profile, name='profile'),
    path('register/', RegisterView.as_view(), name='register'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('logout_success/', logout_success, name='logout_success'),
]
