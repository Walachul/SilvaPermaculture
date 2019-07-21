from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from silvapermaculture.users.forms import UserRegistrationForm, UserLoginForm, UpdateAccountForm
from silvapermaculture.models import User
from silvapermaculture import db, bcrypt
from silvapermaculture.users.utilities import save_picture

users = Blueprint('users', __name__)


@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = UserLoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next') #query parameter
            flash('Logged in successfully!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('index'))#Direct the user to the page he wanted to go when he tried to access it without being logged in, if the next parameter exists.
        else:
            flash('Login unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title= 'Login', form=form)

@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = UserRegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Successfully created account! You can now login.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title= 'Register', form=form)

@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))

@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.profilePic.data:

            picture_file = save_picture(form.profilePic.data)
            current_user.image_file = picture_file#Update user profile picture.

        current_user.username = form.username.data
        db.session.commit()
        flash(f'Your account has been updated!', 'success')
        return redirect(url_for('account')) #User is redirected here so in order to avoid POST-GET redirect pattern. Browser sends GET req, not POST
    elif request.method == 'GET':
        form.username.data = current_user.username
    image_file = url_for('static', filename='img/profile_user/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)