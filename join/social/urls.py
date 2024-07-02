from django.urls import path
from . import views

app_name = 'social'

urlpatterns = [
    path('google/login/', views.google_login, name='google_login'),
    path('github/login/', views.github_login, name='github_login'),
    path('google/callback/', views.google_callback, name='google_callback'),
    path('github/callback/', views.github_callback, name='github_callback'),
]
