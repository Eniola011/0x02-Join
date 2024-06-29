import requests
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()

def create_or_get_user(email, name):
    user, created = User.objects.get_or_create(username=email, defaults={'first_name': name})
    if created:
        user.set_unusable_password()
        user.save()
    return user

def get_google_user_info(access_token):
    user_info_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    user_info_params = {'access_token': access_token}
    user_info_r = requests.get(user_info_url, params=user_info_params)
    return user_info_r.json()

def get_github_user_info(access_token):
    user_info_url = "https://api.github.com/user"
    user_info_headers = {'Authorization': f'token {access_token}'}
    user_info_r = requests.get(user_info_url, headers=user_info_headers)
    return user_info_r.json()

def get_github_user_email(access_token):
    emails_url = "https://api.github.com/user/emails"
    user_info_headers = {'Authorization': f'token {access_token}'}
    emails_r = requests.get(emails_url, headers=user_info_headers)
    emails = emails_r.json()
    return next(email['email'] for email in emails if email['primary'])
