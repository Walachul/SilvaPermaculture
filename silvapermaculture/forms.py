from flask import request
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.ext.sqlalchemy.fields import  QuerySelectMultipleField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from silvapermaculture.models import User, Plants, DNA,NFN



