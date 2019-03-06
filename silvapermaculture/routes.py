from flask import render_template, url_for, flash, redirect
from silvapermaculture import app
from silvapermaculture.forms import UserRegistrationForm, UserLoginForm


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
    form = UserLoginForm()
    return render_template('login.html', title= 'Login', form=form)
@app.route("/register", methods=['GET', 'POST'])
def register():
    form = UserRegistrationForm()
    if form.validate_on_submit():
        flash(f'Successfully created account for {form.username.data}! You can now login.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title= 'Register', form=form)
@app.route("/contact")
def contact():
    return render_template('contact.html', title= 'Contact')