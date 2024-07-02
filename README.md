# Join-Webstack-Portfolio Project
This project is an ALX final portfolio project to mark the end of the backend specialization. It is a user authentication system that allows users to sign up, log in, and log out using their email, Google, and GitHub accounts.

## Table of Contents
- Project Overview
- Features
- Prerequisites and Configuration
- Setup Instructions
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

7. Set Up OAuth2 Credentials:
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
