from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.ext.sqlalchemy.fields import  QuerySelectMultipleField
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
#Query for Dynamic Nutrient Accumulator Model for QuerySelectMultipleField
def enabled_dna():
    return DNA.query
#Query for Nitrogen Fixers Nursing Model for QuerySelectMultipleField
def enabled_nfn():
    return NFN.query

class NewPlantForm(FlaskForm):
    common_name = StringField('Common Name', render_kw={"placeholder": "Common name"},
                              validators=[DataRequired(), Length(min=2, max=40)])
    botanical_name = StringField('Botanical Name', render_kw={"placeholder": "Botanical name"},
                                 validators=[DataRequired(), Length(min=2, max=80)])
    short_description = TextAreaField('Short Description', render_kw={"placeholder": "Please add a short description"},
                                      validators=[DataRequired()])
    medicinal = TextAreaField('Medicinal Use', render_kw={"placeholder": "Medicinal use"},
                            validators=[DataRequired()])
    dna = QuerySelectMultipleField('Select Element',query_factory=enabled_dna,allow_blank=True, get_label='element')
    nfn = QuerySelectMultipleField('Select Property',query_factory=enabled_nfn,allow_blank=True, get_label='plant_extra')

    submit = SubmitField('Add plant')

class UpdatePlantForm(FlaskForm):
    common_name = StringField('Common Name', render_kw={"placeholder": "Common name"},
                              validators=[DataRequired(), Length(min=2, max=40)])
    botanical_name = StringField('Botanical Name', render_kw={"placeholder": "Botanical name"},
                                 validators=[DataRequired(), Length(min=2, max=80)])
    short_description = TextAreaField('Short Description', render_kw={"placeholder": "Please add a short description"},
                                      validators=[DataRequired()])
    medicinal = TextAreaField('Medicinal Use', render_kw={"placeholder": "Medicinal use"},
                            validators=[DataRequired()])
    plantPic = FileField('Update Plant Picture', validators=[FileAllowed(['jpg', 'png'])])
    dna = QuerySelectMultipleField('Select Element',query_factory=enabled_dna,allow_blank=True, get_label='element')
    nfn = QuerySelectMultipleField('Select Property',query_factory=enabled_nfn,allow_blank=True, get_label='plant_extra')
    submit = SubmitField('Update')

class SearchForm(FlaskForm):
    search_common = StringField('Search', render_kw={"placeholder": "Common name"})
    search_botanical = StringField('Botanical Name', render_kw={"placeholder": "Botanical name"})
    filter_dna = QuerySelectMultipleField('Filter by nutrient',query_factory=enabled_dna,allow_blank=True, get_label='element')
    filter_nfn = QuerySelectMultipleField('Filter by properties ', query_factory=enabled_nfn, allow_blank=True,
                                   get_label='plant_extra')
    submit = SubmitField('Search')



