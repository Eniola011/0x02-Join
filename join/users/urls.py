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
from .views import (
    CustomPasswordResetView,
    CustomPasswordResetDoneView,
    CustomPasswordResetConfirmView,
    CustomPasswordResetCompleteView
)
from .views import (
    GoogleLoginView,
    GoogleCallbackView,
    GitHubLoginView,
    GitHubCallbackView
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
    # password reset
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', CustomPasswordResetDoneView.as_view(), name='reset_done'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='reset_confirm'),
    path('reset/done/', CustomPasswordResetCompleteView.as_view(), name='reset_complete'),
    # socialaccounts
    path('oauth/google/login/', GoogleLoginView.as_view(), name='google_login'),
    path('oauth/google/callback/', GoogleCallbackView.as_view(), name='google_callback'),
    path('oauth/github/login/', GitHubLoginView.as_view(), name='github_login'),
    path('oauth/github/callback/', GitHubCallbackView.as_view(), name='github_callback'),
]
