from __future__ import print_function

import json
import os
import pickle
import smtplib, ssl
from firebase_admin import db, firestore, credentials, initialize_app

import base64
import mimetypes
import os
from email.message import EmailMessage
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.text import MIMEText

import google.auth
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.errors import HttpError
from google.auth.transport.requests import Request

import errors

# TODO: FIX LINE 141
SCOPES = [
             "https://www.googleapis.com/auth/gmail.send",
             "https://www.googleapis.com/auth/gmail.compose"
          ]

creds = None

if os.path.exists("auth/token.pickle"):
    with open("auth/token.pickle", 'rb') as token:
        creds = pickle.load(token)

if not os.path.exists("auth/client_id.json"):
    raise Warning("Missing credentials: client_id.json. You will not be able to upload comics or send subscriber emails.")


if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            "auth/client_id.json", SCOPES
        )
        creds = flow.run_local_server(port=0)

    with open("auth/token.pickle", 'wb') as token:
        pickle.dump(creds, token)

def create_email_with_attachment(recipent, sender, subject, attachment_filename, text_content):
    """Create and insert a draft email with attachment.
       Print the returned draft's message and id.
      Returns: Draft object, including draft id and message meta data.

      Load pre-authorized user credentials from the environment.
      TODO(developer) - See https://developers.google.com/identity
      for guides on implementing OAuth2 for the application.
    """

    try:
        # create gmail api client
        service = build('gmail', 'v1', credentials=creds)
        mime_message = EmailMessage()

        # headers
        mime_message['To'] = recipent
        mime_message['From'] = sender
        mime_message['Subject'] = subject

        # text
        mime_message.set_content(text_content)

        # guessing the MIME type
        if attachment_filename:
            type_subtype, _ = mimetypes.guess_type(attachment_filename)
            maintype, subtype = type_subtype.split('/')

            with open(attachment_filename, 'rb') as fp:
                attachment_data = fp.read()

            mime_message.add_attachment(attachment_data, maintype, subtype)

        encoded_message = base64.urlsafe_b64encode(mime_message.as_bytes()).decode()

        create_draft_request_body = {
            'message': {
                'raw': encoded_message
            }
        }
        # pylint: disable=E1101
        draft = service.users().drafts().create(userId="me",
                                                body=create_draft_request_body)\
            .execute()
        print(F'Draft id: {draft["id"]}\nDraft message: {draft["message"]}')

    except HttpError as error:
        print(F'An error occurred: {error}')
        draft = None
        
    return {'raw': base64.urlsafe_b64encode(mime_message.as_string().replace('message','resource').encode('ascii')).decode()}


def build_file_part(file):
    """Creates a MIME part for a file.

    Args:
      file: The path to the file to be attached.

    Returns:
      A MIME part that can be attached to a message.
    """
    content_type, encoding = mimetypes.guess_type(file)

    if content_type is None or encoding is not None:
        content_type = 'application/octet-stream'
    main_type, sub_type = content_type.split('/', 1)
    if main_type == 'text':
        with open(file, 'rb'):
            msg = MIMEText('r', _subtype=sub_type)
    elif main_type == 'image':
        with open(file, 'rb'):
            msg = MIMEImage('r', _subtype=sub_type)
    elif main_type == 'audio':
        with open(file, 'rb'):
            msg = MIMEAudio('r', _subtype=sub_type)
    else:
        with open(file, 'rb'):
            msg = MIMEBase(main_type, sub_type)
            msg.set_payload(file.read())
    filename = os.path.basename(file)
    msg.add_header('Content-Disposition', 'attachment', filename=filename)
    return msg

def send_email(recipent, sender, subject, text_content, attachment_filename=None):
    """Create and send an email message
    Print the returned  message id
    Returns: Message object, including message id

    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.
    """

    try:
        if not creds:
            raise errors.MissingCredentialsWarning()

        service = build('gmail', 'v1', credentials=creds)
        message = create_email_with_attachment(recipent, sender, subject, attachment_filename, text_content)

        # pylint: disable=E1101
        send_message = (service.users().messages().send
                        (userId="me", body=message).execute())
        print(F'Message Id: {send_message["id"]}')

    except HttpError as error:
        print(F'An error occurred: {error}')
        send_message = None

    return send_message

def send_emails(comic):
    try:
        cred = credentials.Certificate("auth/admin_key.json")
    except FileNotFoundError as e:
        raise errors.MissingCredentialsWarning("Credentials do not exist. Please check that you have admin_key.json in the auth directory.") from e

    app = initialize_app(cred)

    store = firestore.client()
    doc_ref = store.collection(u"emails")

    docs = doc_ref.get()

    with open("dev/comic_num.txt", 'r') as f:
        comic_num = f.read()

    for user in docs:
        email = user.to_dict()["email"]
        first_name = user.to_dict()["firstName"].capitalize()

        send_email(email, "Do Not Reply - Riche$t Fine$t Notifier", f"Do Not Reply - Riche$t Fine$t #{comic_num}", 
        f"Hello {first_name},\n\nRiche$t Fine$t #{comic_num} has been uploaded! You can read the comic in the email's attachments, or, alternatively, go to https://richestfinest.github.io\n\nHappy Reading!\nRiche$t Fine$t Team",
        comic)

def send_custom_emails(subject, text):
    try:
        cred = credentials.Certificate("auth/admin_key.json")
    except FileNotFoundError as e:
        raise errors.MissingCredentialsWarning("Credential admin_key.json does not exist. Please check that you have admin_key.json in the auth directory.") from e
        
    app = initialize_app(cred)

    store = firestore.client()
    doc_ref = store.collection(u"emails")

    docs = doc_ref.get()

    for user in docs:
        email = user.to_dict()["email"]
        first_name = user.to_dict()["firstName"].capitalize()

        send_email(email, "Do Not Reply - Riche$t Fine$t Notifier", subject, text.replace("[name]", first_name))
