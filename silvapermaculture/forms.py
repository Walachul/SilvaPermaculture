from flask import request
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.ext.sqlalchemy.fields import  QuerySelectMultipleField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from silvapermaculture.models import User, Plants, DNA,NFN

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
    other_uses = TextAreaField('Other uses', render_kw={"placeholder": "Other uses. Example: It is tolerant"
                                                                       " of being cut several times a year and"
                                                                       " can be used to provide 'instant compost' for crops."})
    habitats = TextAreaField("Habitats", render_kw={"placeholder": "Please write a habitat."
                                                                   " Example: Shady spots, Partial/Full Sun."})
    region = TextAreaField("Region(s)", render_kw={"placeholder": "Please add a region."})
    dna = QuerySelectMultipleField('Select Element',query_factory=enabled_dna,allow_blank=True, get_label='element')
    nfn = QuerySelectMultipleField('Select Property',query_factory=enabled_nfn,allow_blank=True, get_label='plant_extra')
    plantPic = FileField('Update Plant Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Add plant')
    #Check to see if botanical name exists
    def validate_botanical_name(self, botanical_name):
        if botanical_name.data != botanical_name:
            botanical_name = Plants.query.filter_by(botanical_name=botanical_name.data).first()
            if botanical_name:
                raise ValidationError('That botanical name is taken. Please choose another one.')
class UpdatePlantForm(FlaskForm):
    common_name = StringField('Common Name', render_kw={"placeholder": "Common name"},
                              validators=[DataRequired(), Length(min=2, max=40)])
    botanical_name = StringField('Botanical Name', render_kw={"placeholder": "Botanical name"},
                                 validators=[DataRequired(), Length(min=2, max=80)])
    short_description = TextAreaField('Short Description', render_kw={"placeholder": "Please add a short description"},
                                      validators=[DataRequired()])
    medicinal = TextAreaField('Medicinal Use', render_kw={"placeholder": "Medicinal use"},
                            validators=[DataRequired()])
    other_uses = TextAreaField('Other uses', render_kw={"placeholder": "Example:The plant grows very quickly, "
                                                                       "producing a lot of bulk. It is tolerant"
                                                                       " of being cut several times a year and"
                                                                       " can be used to provide 'instant compost' for crops."})
    habitats = TextAreaField("Habitats", render_kw={"placeholder": "Example: Shady spots, Partial/Full Sun."})
    region = TextAreaField("Region(s)", render_kw={"placeholder": "Please add a region."})
    plantPic = FileField('Update Plant Picture', validators=[FileAllowed(['jpg', 'png'])])
    dna = QuerySelectMultipleField('Select Element',query_factory=enabled_dna,allow_blank=True, get_label='element')
    nfn = QuerySelectMultipleField('Select Property',query_factory=enabled_nfn,allow_blank=True, get_label='plant_extra')
    submit = SubmitField('Update')

    # Check to see if botanical name exists
    def validate_botanical_name(self, botanical_name):
        if botanical_name.data != botanical_name:
            botanical_name = Plants.query.filter_by(botanical_name=botanical_name.data).first()
            if botanical_name:
                raise ValidationError('That botanical name is taken. Please choose another one.')

class SearchForm(FlaskForm):
    q = StringField(('Search plant'), validators=[DataRequired(),Length(max=60)])

    def __init__(self, *args, **kwargs):
        #The formdata arg determines from where Flask forms gets submissions.
        if 'formdata' not in kwargs:
            kwargs['formdata'] = request.args
        if 'csrf_enabled' not in kwargs:
            kwargs['csrf_enabled'] = False
        super(SearchForm, self).__init__(*args, **kwargs)
    submit = SubmitField('Search')

#Filtered Search Form for Dynamic Nutrients Accumulators
class SearchFormN(FlaskForm):

    dna = QuerySelectMultipleField('Select Element', validators=[DataRequired()], query_factory=enabled_dna, allow_blank=True, get_label='element')
    nfn = QuerySelectMultipleField('Select Property', validators=[DataRequired()], query_factory=enabled_nfn, allow_blank=True,
                                   get_label='plant_extra')
    def __init__(self, *args, **kwargs):
        if 'formdata' not in kwargs:
            kwargs['formdata'] = request.args
        if 'csrf_enabled' not in kwargs:
            kwargs['csrf_enabled'] = False
        super(SearchFormN, self).__init__(*args, **kwargs)
    submit = SubmitField('Search')

