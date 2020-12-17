#!/usr/bin/env python3

import connexion
from flask_sqlalchemy import SQLAlchemy
from config import Config
from swagger_server import encoder
from flask_cors import CORS
from flask_migrate import Migrate

app = connexion.App(__name__, specification_dir='./swagger/')
application = app.app
application.json_encoder = encoder.JSONEncoder
application.config.from_object(Config)
db = SQLAlchemy(application)
migrate = Migrate(application, db)
CORS(application, supports_credentials=True)
app.add_api('swagger.yaml', arguments={'title': 'Phlebology helper Project'})

