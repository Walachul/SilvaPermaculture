import logging
import os
from logging.handlers import RotatingFileHandler
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from config import Config
from elasticsearch import Elasticsearch



db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'



def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    # Check to see if URL for Esearch is configured. If not, disable Esearch and the app can still run.
    app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']]) \
        if app.config['ELASTICSEARCH_URL'] else None
    from silvapermaculture.users.routes import users  # This is imported here to avoid circular imports.
    from silvapermaculture.plants.routes import plants  # This is imported here to avoid circular imports.
    from silvapermaculture.main.routes import main  # This is imported here to avoid circular imports.
    from silvapermaculture.errors.handlers import errors
    app.register_blueprint(users)
    app.register_blueprint(plants)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    if app.config['LOG_TO_STDOUT']:
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)
        app.logger.addHandler(stream_handler)
    else:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/silvapermaculture.log',
                                           maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s '
            '[in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('Silvapermaculture startup')

    return app

with app.app_context():
    db.create_all()