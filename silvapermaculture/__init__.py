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
#Heroku deploymenet

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

from silvapermaculture import routes #This is imported here to avoid circular imports.