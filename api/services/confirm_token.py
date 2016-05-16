from flask import current_app, render_template, url_for
from itsdangerous import URLSafeTimedSerializer

from api.services import mail as mail_service


def generate_confirmation_token(email):
	serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
	return serializer.dumps(email, salt=current_app.config['SECURITY_PASSWORD_SALT'])


def confirm_token(token, expiration=3600):
	serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
	try:
		email = serializer.loads(
			token,
			salt=current_app.config['SECURITY_PASSWORD_SALT'],
			max_age=expiration
		)
	except Exception as e:
		return False
	return email


def send_confirm_email(email):
	token = generate_confirmation_token(email)
	confirm_url = url_for('api.confirm_email', token=token, _external=True)
	email_body = render_template('confirm_email.html', confirm_url=confirm_url)
	subject = "Prescrisur - Activation"
	return mail_service.send_from_default(email, subject, email_body)
