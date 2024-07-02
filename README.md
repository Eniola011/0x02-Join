# Join-Webstack-Portfolio Project
- ALX final portfolio project to mark the end of backend specialization.

# Table of Contents
### Project Overview
- Join project is a user authentication system allows users to sign up, log in, log out with their email, google and github accounts respectively.

### Features
- User registration with email verification link.
- Signup/Signin with github account, google account.
- Login and logout functionality.
- Account activation through email confirmation.

### Prerequisites and Configuration.
- Ubuntu-20.04 terminal
- Django
- 

### Setup Instructions
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
   - Download the credentials JSON file.

8. 
