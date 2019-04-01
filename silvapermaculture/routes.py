import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from silvapermaculture import app, db, bcrypt
from silvapermaculture.forms import UserRegistrationForm, UserLoginForm, UpdateAccountForm, NewPlantForm, UpdatePlantForm
from silvapermaculture.models import User, Plants
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


#Route for users to add a plant to the database
@app.route("/plants/new/", methods=['GET', 'POST'])
@login_required# User must be logged in to create a new plant
def new_plant():
    form = NewPlantForm()

    if form.validate_on_submit():
        new_plant = Plants(common_name = form.common_name.data, botanical_name = form.botanical_name.data,
                           short_description = form.short_description.data, medicinal=form.medicinal.data,
                           author=current_user)
        for dna_element in form.dna.data:
            new_plant.dna.append(dna_element)

        for nfn_element in form.nfn.data:
            new_plant.nfn.append(nfn_element)

        db.session.add(new_plant)
        db.session.commit()
        flash(f'Thank you ! You have successfully added a plant to the database!', 'success')
        return redirect(url_for('plants'))
    image_file = url_for('static', filename='img/plants/default_plant_pic.jpg')
    return render_template('new_plant.html', title='Add new plant',
                           image_file=image_file, form=form, header="Add a new plant")

#Go to specific plant with a specific ID
@app.route("/plants/<int:plant_id>")
def plant(plant_id):
    plant = Plants.query.get_or_404(plant_id)
    return render_template('plant.html', title=plant.common_name, plant=plant)
#Function for updating default plant, scale it and use hex
def save_plant_picture(form_plantPic):
    """
    Change img filename to be a random hex, instead of keeping the original name of the file,
    in order to avoid having files with the same name.
    """
    random_hex_image = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_plantPic.filename)
    picture_fn = random_hex_image + f_ext
    picture_path = os.path.join(app.root_path, 'static/img/plants', picture_fn) #Saving the new plantPic to the specified folder.
    scale_image = (250, 180)
    img_new = Image.open(form_plantPic)
    img_new.thumbnail(scale_image)
    img_new.save(picture_path)
    return picture_fn

#Edit a plant with a specific ID
@app.route("/plants/<int:plant_id>/edit", methods=['GET', 'POST'])
@login_required# User must be logged in to create a new plant
def update_plant(plant_id):
    plant = Plants.query.get_or_404(plant_id)
    #Check to see if the user who wants to update an existing plant is the actual logged user
    if plant.author != current_user:
        abort(403)
    form = UpdatePlantForm()
    #Update plant with new data from form fields
    if form.validate_on_submit():
        if form.plantPic.data:
            picture_file = save_plant_picture(form.plantPic.data)
            plant.image_file = picture_file

        plant.common_name = form.common_name.data
        plant.botanical_name = form.botanical_name.data
        plant.short_description = form.short_description.data
        plant.medicinal = form.medicinal.data
        plant.dna = form.dna.data
        plant.nfn = form.nfn.data
        db.session.commit()
        flash(f'You have successfully updated the plant !', 'success')
        return redirect(url_for('plant', plant_id=plant.id))
    elif request.method == 'GET':
        #Form is filled with the current data for a plant
        form.common_name.data = plant.common_name
        form.botanical_name.data = plant.botanical_name
        form.short_description.data = plant.short_description
        form.medicinal.data = plant.medicinal
        form.dna.data = plant.dna
        form.nfn.data = plant.nfn
    image_file = url_for('static', filename='img/plants/default_plant_pic.jpg')
    return render_template('update_plant.html', title='Update plant', image_file=image_file,
                           form=form, header ="Update a plant")

@app.route("/contact")
def contact():
    return render_template('contact.html', title= 'Contact')