import os
import base64
from email.mime.text import MIMEText
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/gmail.send']
REDIRECT_URI = 'http://localhost:8000/'

def get_credentials():
    creds = None
    print("Checking for existing token.json...")
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception as e:
                print(f"Error refreshing token: {e}")
                os.remove('token.json')
                creds = None
    if not creds or not creds.valid:
        print("Running OAuth flow to get new token...")
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES, redirect_uri=REDIRECT_URI
        )
        auth_url, _ = flow.authorization_url(prompt='consent')
        print(f"Please go to this URL: {auth_url}")
        code = input("Enter the authorization code: ")
        try:
            flow.fetch_token(code=code)
        except Exception as e:
            print(f"Error fetching token: {e}")
            return None
        creds = flow.credentials
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
            print("Token saved to token.json")
    return creds

def send_email(to, subject, body):
    creds = get_credentials()
    if not creds:
        print("Failed to obtain credentials")
        return

    try:
        service = build('gmail', 'v1', credentials=creds)
        message = MIMEText(body)
        message['to'] = to
        message['subject'] = subject
        raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
        message = {'raw': raw}
        send_message = service.users().messages().send(userId="me", body=message).execute()
        print("Email sent")
        return send_message
    except Exception as e:
        print(f"Error sending email: {e}")

#if __name__ == "__main__":
#    send_email("eniolaagbalu@gmail.com", "Test Subject", "Test Body")
