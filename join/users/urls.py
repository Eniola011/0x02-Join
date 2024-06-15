from django.urls import path
from .views import homepage, CustomLoginView, RegisterView, CustomPasswordResetView

urlpatterns = [
    path('', homepage, name='home'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('reset_password/', CustomPasswordResetView.as_view(), name='password_reset'),
]
