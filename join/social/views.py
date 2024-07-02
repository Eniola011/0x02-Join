import os
import requests
from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth import login
from django.contrib.auth.models import User

# Create your views here.

# Constants for Google
GOOGLE_CLIENT_ID = '518015513334-bqe43jlua4nqpuhhqea10mf3t5d8atoc.apps.googleusercontent.com'
GOOGLE_CLIENT_SECRET = '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'
GOOGLE_REDIRECT_URI = 'http://localhost:8000/social/google/callback/'

# Constants for GitHub
GITHUB_CLIENT_ID = 'Ov23linOr8y4JNoIrRUa'
GITHUB_CLIENT_SECRET = 'b9ec5eea11d50c5a24fe22da7dc4527a8242089b'
GITHUB_REDIRECT_URI = 'http://localhost:8000/social/github/callback/'

def google_login(request):
    auth_url = (
        f"https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={GOOGLE_CLIENT_ID}"
        f"&redirect_uri={GOOGLE_REDIRECT_URI}&scope=email%20profile&access_type=offline&prompt=consent"
    )
    return redirect(auth_url)

def google_callback(request):
    code = request.GET.get('code')
    token_url = 'https://oauth2.googleapis.com/token'
    token_data = {
        'code': code,
        'client_id': GOOGLE_CLIENT_ID,
        'client_secret': GOOGLE_CLIENT_SECRET,
        'redirect_uri': GOOGLE_REDIRECT_URI,
        'grant_type': 'authorization_code'
    }
    token_response = requests.post(token_url, data=token_data)
    token_json = token_response.json()
    access_token = token_json.get('access_token')
    userinfo_url = 'https://www.googleapis.com/oauth2/v2/userinfo'
    userinfo_response = requests.get(userinfo_url, headers={'Authorization': f'Bearer {access_token}'})
    userinfo = userinfo_response.json()
    
    user, created= User.objects.get_or_create(username=userinfo['email'], defaults={'email': userinfo['email']})
    if created:
        user.set_unusable_password()
        user.save()
    
    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
    return redirect('users:profile')

def github_login(request):
    auth_url = (
        f"https://github.com/login/oauth/authorize?client_id={GITHUB_CLIENT_ID}"
        f"&redirect_uri={GITHUB_REDIRECT_URI}&scope=read:user user:email"
    )
    return redirect(auth_url)

def github_callback(request):
    code = request.GET.get('code')
    token_url = 'https://github.com/login/oauth/access_token'
    token_data = {
        'code': code,
        'client_id': GITHUB_CLIENT_ID,
        'client_secret': GITHUB_CLIENT_SECRET,
        'redirect_uri': GITHUB_REDIRECT_URI,
    }
    headers = {'Accept': 'application/json'}
    token_response = requests.post(token_url, data=token_data, headers=headers)
    token_json = token_response.json()
    access_token = token_json.get('access_token')
    
    userinfo_url = 'https://api.github.com/user'
    userinfo_response = requests.get(userinfo_url, headers={'Authorization': f'token {access_token}'})
    userinfo = userinfo_response.json()
    
    emails_url = 'https://api.github.com/user/emails'
    emails_response = requests.get(emails_url, headers={'Authorization': f'token {access_token}'})
    emails = emails_response.json()
    primary_email = next(email['email'] for email in emails if email['primary'])
    
    user, created= User.objects.get_or_create(username=primary_email, defaults={'email': primary_email})
    if created:
        user.set_unusable_password()
        user.save()
    
    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
    return redirect('users:profile')
