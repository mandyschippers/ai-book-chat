from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS, cross_origin

app = Flask(__name__, static_folder='../client/build', static_url_path='')
app.config.from_object('config.Config')

db = SQLAlchemy(app)
migrate = Migrate(app, db)
cors = CORS(app)

from app import routes