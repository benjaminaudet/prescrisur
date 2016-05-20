from flask import Flask
from flask_mail import Mail
from flask.ext.cors import CORS
from flask.ext.login import LoginManager

from api.config import *
from json_encoder import ModelJSONEncoder

mail = Mail()
cors = CORS()
login_manager = LoginManager()


def create_app(config_module):
	# Create app and set config
	app_ = MyFlask(__name__)
	app_.json_encoder = ModelJSONEncoder
	app_.config.from_object(config_module)
	app_.set_static_folder()

	# Import views
	from views import api
	app_.register_blueprint(api)

	# Init plugins
	mail.init_app(app_)
	cors.init_app(app_)
	login_manager.init_app(app_)
	return app_


app = create_app(EnvConfig)
