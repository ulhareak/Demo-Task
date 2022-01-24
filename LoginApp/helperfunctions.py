

from django.core.mail import send_mail

from django.conf import settings

class UserInfo:
    def __init__(self , username  , token):
        self.username = username
        self.token = token



def send_forgertpassword_email(email, token):
    subject = 'Your forget password link'
    message = f'Hi , click on the link to reset your password http://127.0.0.1:8000/changepassword/{token}/'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
    return True
