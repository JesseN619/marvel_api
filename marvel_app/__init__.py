from flask import Flask
from config import Config
from .authentication.routes import auth
from .site.routes import site

app = Flask(__name__)
app.config.from_object(Config)

app.register_blueprint(site)
app.register_blueprint(auth)
