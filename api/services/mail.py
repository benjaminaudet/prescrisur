import bleach
from flask_mail import Message
from flask import current_app

from api import mail


def send(data):
	subject = bleach.clean(data['subject'])
	body = bleach.clean(data['body'])
	sender = (data['sender']['name'], data['sender']['email'])
	msg = Message(subject=subject, body=body, sender=sender, recipients=[current_app.config['DEFAULT_RECIPIENT']])
	mail.send(msg)
