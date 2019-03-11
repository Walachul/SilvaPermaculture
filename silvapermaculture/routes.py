import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from silvapermaculture import app, db, bcrypt
from silvapermaculture.forms import UserRegistrationForm, UserLoginForm, UpdateAccountForm, NewPlantForm
from silvapermaculture.models import User, Plants, Medicinal_Use, Dynamic_Nutrient_Accumulated, Nitrogen_Fixers_Nursing
from flask_login import login_user, current_user, logout_user, login_required

#Routes
@app.route("/")
@app.route("/index")
def index():
    return render_template('index.html')
@app.route("/plants")
def plants():
    plants = Plants.query.all()
    return render_template('plants.html', title= 'Plants Database', plants=plants)
@app.route("/statistics")
def statistics():
    return render_template('statistics.html', title= 'Statistics')
@app.route("/about")
def about():
    return render_template('about.html', title= 'About')
@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = UserLoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next') #query parameter
            flash('Logged in successfully.', 'success')
            return redirect(next_page) if next_page else redirect(url_for('index'))#Direct the user to the page he wanted to go when he tried to access it without being logged in, if the next parameter exists.
        else:
            flash('Login unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title= 'Login', form=form)

@app.route("/register", methods=['GET', 'POST'])
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

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))

def save_picture(form_profilePic):
    """
    Change img filename to be a random hex, instead of keeping the original name of the file,
    in order to avoid having files with the same name.
    """
    random_hex_image = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_profilePic.filename)
    picture_fn = random_hex_image + f_ext
    picture_path = os.path.join(app.root_path, 'static/img/profile_user', picture_fn) #Saving the new profilePic to the specified folder.
    scale_image = (125, 75)
    img_new = Image.open(form_profilePic)
    img_new.thumbnail(scale_image)
    img_new.save(picture_path)
    return picture_fn

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.profilePic.data:
            existing_profile_img = current_user.image_file
            picture_file = save_picture(form.profilePic.data)
            current_user.image_file = picture_file#Update user profile picture.
            if existing_profile_img is not None:#Deleting old image of the user after updating
                existing_profile_img_path= os.path.join(app.root_path, 'static/img/profile_user', existing_profile_img)
                os.remove(existing_profile_img_path)
        current_user.username = form.username.data
        db.session.commit()
        flash(f'Your account has been updated!', 'success')
        return redirect(url_for('account')) #User is redirected here so in order to avoid POST-GET redirect pattern. Browser sends GET req, not POST
    elif request.method == 'GET':
        form.username.data = current_user.username
    image_file = url_for('static', filename='img/profile_user/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)


#Router for users to add a plant to the database
@app.route("/plants/new", methods=['GET', 'POST'])
@login_required# User must be logged in to create a new plant
def new_plant():
    form = NewPlantForm()
    if form.validate_on_submit():
        new_plant = Plants(common_name = form.common_name.data, botanical_name = form.botanical_name.data, short_description = form.short_description.data, author=current_user)
        db.session.add(new_plant)
        db.session.commit()
        flash(f'Thank you ! You have successfully added a plant to the database!', 'success')
        return redirect(url_for('plants'))
    image_file = url_for('static', filename='img/plants/default_plant_pic.jpg')
    return render_template('new_plant.html', title='Add new plant', image_file=image_file, form=form)
#Go to specific plant with a specific ID
@app.route("/plants/<int:plants_id>")
def plant(plants_id):
    plant = Plants.query.get_or_404(plants_id)
    return render_template('plant.html', title=plant.common_name, plant=plant)

@app.route("/contact")
def contact():
    return render_template('contact.html', title= 'Contact')