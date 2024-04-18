import os
import pickle
import base64
import pandas as pd
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import googleapiclient
from bs4 import BeautifulSoup

from classifier import urgency


SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/gmail.labels', 'https://www.googleapis.com/auth/gmail.modify']

def get_credentials():
    """Retrieve credentials from token.pickle or generate new one if needed."""
    creds = None
    if os.path.exists('toke.pickle'):
        with open('toke.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credential.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('toke.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return creds

def create_custom_labels(service):
    """Create custom labels if they don't exist."""
    labels = ['VeryUrgent', 'Urgent', 'Neutral', 'NotUrgent']
    existing_labels = service.users().labels().list(userId='me').execute()
    existing_label_names = [label['name'] for label in existing_labels['labels']]

    for label in labels:
        if label not in existing_label_names:
            body = {'name': label, 'labelListVisibility': 'labelShow', 'messageListVisibility': 'show'}
            service.users().labels().create(userId='me', body=body).execute()

def assign_labels_to_emails(service, emails):
    """Assign labels to emails."""
    # Read the label data from the CSV file
    label = pd.read_csv('updated_email.csv')
    
    # Iterate over emails and corresponding urgency levels
    for email, urgency in zip(emails, label['urgency']):
        label_name = None
        if pd.notnull(urgency):
            label_name = urgency
            print(label_name) # Assuming labels are named like "Urgency_1", "Urgency_2", etc.
        else:
            print(f"No urgency level found for email: {email['mail_id']}")
            continue

        # Get the label ID for the current label name
        labels = service.users().labels().list(userId='me').execute()['labels']
        label_id = None
        for label_info in labels:
            if label_info['name'] == label_name:
                label_id = label_info['id']
                break
        
        # Assign the label to the email if the label exists
        if label_id:
            message_id = email['mail_id']
            service.users().messages().modify(userId='me', id=message_id, body={'addLabelIds': [label_id]}).execute()
        else:
            print(f"Label '{label_name}' not found.")


def get_emails():
    """Get emails from Gmail"""
    creds = get_credentials()
    if creds is None:
     print("Authentication failed.")
    else:
     service = build('gmail', 'v1', credentials=creds)
    print(1) 
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
                description = soup.get_text()

            for header in msg['payload']['headers']:
                if header['name'] == 'Subject':
                    subject = header['value']
            
            # Append mail_id and label to emails
            emails.append({'mail_id': message['id'], 'title': subject, 'description': description})

        nextPageToken = results.get('nextPageToken')
        if not nextPageToken:
            break  # No more pages, exit the loop
        page_count += 1  # Increment page count 
    df = pd.DataFrame(emails)
    df.to_csv('emails.csv', index=False)
    return emails    

  

def label():
 creds = get_credentials()
 if creds is None:
    print("Authentication failed.")
 else:
  service = build('gmail', 'v1', credentials=creds)
  emails = get_emails()
  assign_labels_to_emails(service, emails)
  df = pd.DataFrame(emails)
  df.to_csv('email.csv', index=False)

