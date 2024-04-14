import os
import pickle
import base64
import pandas as pd
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from bs4 import BeautifulSoup
from temp import run_model

# from model.temp import run_model

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def get_emails():
    print("Fetching Emails")
    """Get emails from Gmail"""
    creds = None

    # log in if token.pickle not already generated
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)

    emails = []
    nextPageToken = None
    page_count = 0  # Counter to keep track of fetched pages
    while page_count <= 1:  # Fetch 10 pages worth of emails
        # Gmail API
        results = service.users().messages().list(
            userId='me', labelIds=['INBOX'], pageToken=nextPageToken).execute()
        messages = results.get('messages', [])
        
        # Iterate over messages and process each email
        for message in messages:
            msg = service.users().messages().get(userId='me', id=message['id']).execute()
            subject = ''
            description = ''

            # Check if the email is multipart and extract text/plain part
            if 'parts' in msg['payload']:
                for part in msg['payload']['parts']:
                    mime_type = part['mimeType']
                    if mime_type == 'text/plain':
                        if 'data' in part['body']:
                            description = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
                            break

            # If the email is not multipart or plain text part not found, extract HTML content
            if not description and 'data' in msg['payload']['body']:
                html_content = base64.urlsafe_b64decode(msg['payload']['body']['data']).decode('utf-8')
                soup = BeautifulSoup(html_content, 'html.parser')
                # description = 'HTML content'
                description = soup.get_text()

            for header in msg['payload']['headers']:
                if header['name'] == 'Subject':
                    subject = header['value']
                
            emails.append({'title': subject, 'description': description})
        
        nextPageToken = results.get('nextPageToken')
        if not nextPageToken:
            break  # No more pages, exit the loop
        page_count += 1  # Increment page count

    print(1)
    df = pd.DataFrame(emails)
    df.to_csv('emails.csv', index=False)
    # run_model()
    run_model()
    return emails


    


