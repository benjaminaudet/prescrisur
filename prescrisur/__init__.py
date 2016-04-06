from flask import Flask

app = Flask(__name__)
app.secret_key = 'gEK\xa3n\x80\xc1\x91\xef\x9f>\xf7\xcb\x87:B\x06\xd6\xa3\x1a.\xfc\xb9\xf1'


import prescrisur.views
from db import DB