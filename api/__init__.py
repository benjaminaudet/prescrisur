from flask import Flask
from flask.ext.cors import CORS

from api.json_encoder import ModelJSONEncoder


app = Flask(__name__, template_folder='../front', static_folder='../front')
cors = CORS(app, resources={r"/api/*": {"origins": "http://localhost:8000"}})

app.json_encoder = ModelJSONEncoder
app.secret_key = '\xfb\x1c\xcd\xa4\xdb\xf3\xf8\xd9\xc8\xe9~\xd4\xd0\xf5\xeb\xb3\tSH\xc6\x97e\xbeZ'


import api.views
