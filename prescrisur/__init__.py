from flask import Flask

app = Flask(__name__)
app.secret_key = '\xfb\x1c\xcd\xa4\xdb\xf3\xf8\xd9\xc8\xe9~\xd4\xd0\xf5\xeb\xb3\tSH\xc6\x97e\xbeZ'


import prescrisur.views
import db