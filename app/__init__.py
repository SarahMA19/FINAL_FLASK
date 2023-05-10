from flask import Flask, render_template

from config import Config

from .api.services import api
from .payments.routes import payments

from . models import db
from flask_migrate import Migrate
from flask_cors import CORS

app= Flask(__name__)

CORS(app)

app.config.from_object(Config)

@app.route('/')
def index():
    return render_template('base.html')


db.init_app(app)
migrate = Migrate(app, db)

app.register_blueprint(api)
app.register_blueprint(payments)


