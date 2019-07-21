

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