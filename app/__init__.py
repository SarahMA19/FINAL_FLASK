from flask import Flask
from config import Config
from .api.services import api


from . models import db
from flask_migrate import Migrate
from flask_cors import CORS

app= Flask(__name__)

CORS(app)





app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)

app.register_blueprint(api)

from . import audio
