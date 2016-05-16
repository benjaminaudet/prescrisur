import os


class EnvConfig(object):
	SECRET_KEY = '\xfb\x1c\xcd\xa4\xdb\xf3\xf8\xd9\xc8\xe9~\xd4\xd0\xf5\xeb\xb3\tSH\xc6\x97e\xbeZ'
	SECURITY_PASSWORD_SALT = '\xa3\xfb5=\x03W\x12\\\xc0\x82s\xbb\x85"\xf5\x96\xc6L\xb9\x96\x10M\xea['
	DEFAULT_RECIPIENT = os.environ['DEFAULT_RECIPIENT_EMAIL']
	# Mail Server Configuration
	MAIL_SERVER = 'smtp.gmail.com'
	MAIL_PORT = 465
	MAIL_USE_TLS = False
	MAIL_USE_SSL = True
	MAIL_USERNAME = 'prescrisur@gmail.com'
	MAIL_PASSWORD = 'gabin2014'
	MAIL_DEFAULT_SENDER = 'Prescrisur <no-reply-prescrisur@gmail.com>'
