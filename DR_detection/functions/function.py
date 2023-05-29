from django.core.mail import EmailMessage
from pathlib import Path

import os

BASE_DIR = Path(__file__).resolve().parent.parent

def handle_file_upload(f):
    print('Success')
    with open(os.path.join(BASE_DIR,'project\\DeepRetinopathy\\')+"input_img"+".jpeg", 'wb+') as destination:  
        for chunk in f.chunks():  
            destination.write(chunk)

def send_email_da(subject, message, from_email, recipient_list):
    email = EmailMessage(
        subject=subject,
        body=message,
        from_email=from_email,
        to=recipient_list,
    )
    return email.send()
