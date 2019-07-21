import os


class Config:

    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL')
    PLANTS_PER_PAGE = 5
