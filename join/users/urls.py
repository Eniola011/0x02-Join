from django.urls import path
from django.contrib.auth import views as auth_views
from .views import activate, homepage, CustomLoginView, RegisterView, CustomPasswordResetView

urlpatterns = [
    path('', homepage, name='home'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('register/', RegisterView.as_view(), name='register'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
]
