from flask_wtf import FlaskForm
from wtforms.ext.sqlalchemy.fields import  QuerySelectMultipleField
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from silvapermaculture.models import User, DNA,NFN

class UserRegistrationForm(FlaskForm):
    username = StringField('Username', render_kw={"placeholder": "Username"},
                           validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password',render_kw={"placeholder": "Enter password"},
                             validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',render_kw={"placeholder": "Confirm password"},
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose another one.')


class UserLoginForm(FlaskForm):
    username = StringField('Username', render_kw={"placeholder": "Username"},
                           validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password',render_kw={"placeholder": "Password"}, validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    profilePic = FileField('Update Profile Picture', validators=[FileAllowed(['jpg','png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose another one.')
#Query for Dynamic Nutrient Accumulator Model
def enabled_dna():
    return DNA.query.all()
#Query for Nitrogen Fixers Nursing Model
def enabled_nfn():
    return NFN.query.all()

class NewPlantForm(FlaskForm):
    common_name = StringField('Common Name', render_kw={"placeholder": "Common name"},
                              validators=[DataRequired(), Length(min=2, max=40)])
    botanical_name = StringField('Botanical Name', render_kw={"placeholder": "Botanical name"},
                                 validators=[DataRequired(), Length(min=2, max=80)])
    short_description = TextAreaField('Short Description', render_kw={"placeholder": "Please add a short description"},
                                      validators=[DataRequired()])
    medicinal = TextAreaField('Medicinal Use', render_kw={"placeholder": "Medicinal use"},
                            validators=[DataRequired()])
    dna = QuerySelectMultipleField('Select Element',query_factory=enabled_dna,allow_blank=True)
    nfn = QuerySelectMultipleField('Select Property',query_factory=enabled_nfn,allow_blank=True)
    submit = SubmitField('Add plant')





