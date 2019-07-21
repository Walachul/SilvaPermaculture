from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from silvapermaculture.config import Config
from elasticsearch import Elasticsearch



db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'



def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
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

    return app