from flask import Flask
import flask.ext.login as flask_login

from api.json_encoder import ModelJSONEncoder


app = Flask(__name__, static_folder='../front')

app.json_encoder = ModelJSONEncoder
app.secret_key = '\xfb\x1c\xcd\xa4\xdb\xf3\xf8\xd9\xc8\xe9~\xd4\xd0\xf5\xeb\xb3\tSH\xc6\x97e\xbeZ'

login_manager = flask_login.LoginManager()
login_manager.init_app(app)


import api.views
