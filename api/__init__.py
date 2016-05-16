from flask import Flask
from flask_mail import Mail
from flask.ext.login import LoginManager

from json_encoder import ModelJSONEncoder

mail = Mail()
login_manager = LoginManager()


def create_app(config_module):
	# Create app and set config
	app_ = Flask(__name__)
	app_.json_encoder = ModelJSONEncoder
	app_.config.from_object(config_module)

	from views import api
	app_.register_blueprint(api)

	mail.init_app(app_)
	login_manager.init_app(app_)
	return app_


app = create_app('api.config.EnvConfig')
