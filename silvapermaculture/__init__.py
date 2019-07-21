from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from silvapermaculture.config import Config
from elasticsearch import Elasticsearch

app = Flask(__name__)
app.config.from_object(Config)
#Check to see if URL for Esearch is configured. If not, disable Esearch and the app can still run.
app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']]) \
    if app.config['ELASTICSEARCH_URL'] else None
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from silvapermaculture.users.routes import users #This is imported here to avoid circular imports.
from silvapermaculture.plants.routes import plants #This is imported here to avoid circular imports.
from silvapermaculture.main.routes import main #This is imported here to avoid circular imports.

app.register_blueprint(users)
app.register_blueprint(plants)
app.register_blueprint(main)