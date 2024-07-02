# Join-Webstack-Portfolio Project
This project is an ALX final portfolio project to mark the end of the backend specialization. It is a user authentication system that allows users to sign up, log in, and log out using their email, Google, and GitHub accounts.

## Table of Contents
- Project Overview
- Features
- Prerequisites and Configuration
- Setup Instructions
- Setting Up Google OAuth2
- Setting Up GitHub OAuth2
- Usage
- License

## Project Overview
Join project is a user authentication system that allows users to sign up, log in, and log out using their email, Google, and GitHub accounts. It includes features such as user registration with email verification, login and logout functionality, and account activation through email confirmation.

## Features
- User registration with email verification link.
- Signup/Signin with github account, google account.
- Login and logout functionality.
- Account activation through email confirmation.

## Prerequisites and Configuration.
- Ubuntu-20.04 terminal
- Python 3.x
- Django 4.2.13 or above
- Requests library
- Google OAuth2 and Gmail API libraries

## Setup Instructions
1. Clone this repository

   ```
     https://github.com/Eniola011/0x02-Join.git
   ```

2. Navigate to project directory.

   ```
     cd /0x02-Join/join
   ```

3. Create a python virtual environment.

   ```
     python3 -m nameofenvironment venv
   ```
   
4. Activate virtual environment.
   ```
     source nameofenvironment/bin/activate
   ```
   
5. Install dependencies.
   ```
     pip3 install django
     pip3 install requests
   ```

6. Install the libraries needed to handle Google OAuth2 and the Gmail API.
   
   ```
     pip3 install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
   ```

7. Set Up OAuth2 Credentials: Note this setup is for email confirmation.
   - Go to "Google Cloud Console": https://console.cloud.google.com/
   - Create a project.
   - Search and Enable "Gmail Api" which can be found in `APIs & Services` > `Library`
   - Configure the oauth consent screen: create `app name`, input your mail as `user support email`, `app logo(optional)`, skip `app domain` and `Authorised domains
`, input your mail as `Developer contact information`, save and continue skip `scopes` save and continue input your mail as `Test users` save and continue.
   - Create OAuth2 Credentials: Go to `APIs & Services` > `Credentials`
   - Click on `Create Credentials` and `select OAuth 2.0 Client IDs`. Application type is `web application` add this http://localhost:8000/ to `Authorised redirect URIs
` skip `Authorised JavaScript origins` then click `create`
   - Download the credentials JSON file and save it as credentials.json in your project directory.

8. Run the project.
   
   ```
      python manage.py migrate
      python manage.py runserver
   ```

## Setting Up Google OAuth2
For google account login and signup.
1. Go to Google Cloud Console:  https://console.cloud.google.com/
2. Create another project call it "social."
3. Search for and enable the "Gmail API" and "Google People API" under `APIs & Services` > `Library`
4. Configure the OAuth consent screen:
   - Create an app name, input your email as the user support email.
   - Add an app logo (optional).
   - Skip app domain and authorised domains.
   - Input your email as the developer contact information, save and continue
   - move to `scopes`: add "https://www.googleapis.com/auth/userinfo.email", "https://www.googleapis.com/auth/userinfo.profile" and "https://www.googleapis.com/auth/gmail.send"
   - save and continue, input your email as test users, save and continue.
5. Create OAuth2 credentials:
   - Go to `APIs & Services` > `Credentials`
   - Click on Create Credentials and select OAuth 2.0 Client IDs.
   - Set the application type to Web application.
   - Add http://localhost:8000/ to the Authorised redirect URIs.
   - Skip authorised JavaScript origins.
   - Click Create.
   - Download the credentials JSON file.

## Setting Up GitHub OAuth2
1. Go to GitHub Developer Settings: https://github.com/settings/developers
2. Click on `New OAuth App`
3. Fill in the application details:
   - Application name: Your app name.
   - Homepage URL: http://localhost:8000/
   - Authorization callback URL: http://localhost:8000/social/github/callback/.
4. Click `Register application`
5. You will get a Client ID and Client Secret. Save the "client secret" you won't see again unlike in google.
6. Add these to your Django settings:
   ```
      # In settings.py or .env
      SOCIAL_AUTH_GITHUB_KEY = 'your-client-id'
      SOCIAL_AUTH_GITHUB_SECRET = 'your-client-secret'
   ```

## Usage
1. Register a new user
   - Go to http://localhost:8000/register/ and register with your email. You will receive an email verification link to activate your account.
2. Login with Email
   - Go to http://localhost:8000/login/ and log in with your registered email and password.
3. Login with Google
   - Go to http://localhost:8000/social/google/login/ to log in with your Google account.
4. Login with GitHub
   - Go to http://localhost:8000/social/github/login/ to log in with your GitHub account.
5. Profile Page
   - After logging in, you will be redirected to the profile page.

## License
- This project is licensed under the MIT License.
