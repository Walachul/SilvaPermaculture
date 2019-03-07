from flask import render_template, url_for, flash, redirect
from silvapermaculture import app, db, bcrypt
from silvapermaculture.forms import UserRegistrationForm, UserLoginForm
from silvapermaculture.models import User, Plants, Medicinal_Use, Dynamic_Nutrient_Accumulated, Nitrogen_Fixers_Nursing
from flask_login import login_user, current_user, logout_user



Plants = {
      'author': 'User Hello',
      'commonName': 'Trandafir',
      'botanicalName': 'Rosa Regalis',
      'shortDescription': 'This is a beautiful plant.',
      'dateAdded': 'April 20, 2021'
    }

medicinal_use = {
    'usage':'Stress relief'
}

Dynamic_Nutrient_Accumulated = {
    'N': 'True',
    'P': 'True',
    'K': 'False',
    'Ca': 'True',
    'Mg': 'True'
}
Nitrogen_Fixers_Nursing = {
    'nursery': 'True',
    'check_nitrogen': 'False',
    'comment': 'This plant works best in full sunlight and requires lot of water.'
}



#Routes
@app.route("/")
@app.route("/index")
def index():
    return render_template('index.html')
@app.route("/plants")
def plants():
    return render_template('plants.html', title= 'Plants', plant=Plants, meds=medicinal_use, dna=Dynamic_Nutrient_Accumulated, nfn=Nitrogen_Fixers_Nursing)
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
            flash('Logged in successfully.', 'success')
            return redirect(url_for('index'))
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

@app.route("/account")
def account():

    return render_template('account.html', title='Account')


@app.route("/contact")
def contact():
    return render_template('contact.html', title= 'Contact')