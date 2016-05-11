import os


class EnvConfig(object):
	DEFAULT_RECIPIENT = os.environ['DEFAULT_RECIPIENT_EMAIL']
	# Mail Server Configuration
	MAIL_SERVER = 'smtp.gmail.com'
	MAIL_PORT = 465
	MAIL_USE_TLS = False
	MAIL_USE_SSL = True
	MAIL_USERNAME = 'pboutruche@octo.com'
	MAIL_PASSWORD = 'rikpied1'
