from flask import Flask 
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
import os 
# import requests
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import MetaData
from datetime import timedelta

#naming conventions for database constraints -- ensures consistent naming across db schema 
metadata = MetaData(naming_convention={
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_`%(constraint_name)s`",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
    })

db = SQLAlchemy(metadata=metadata)
app = Flask(__name__)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)

# Database connection parameters
load_dotenv()
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')
db.init_app(app)
app.secret_key = os.environ.get("SESSIONS_SECRET_KEY")

app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=1)

app.config['SESSION_COOKIE_SECURE'] = True

