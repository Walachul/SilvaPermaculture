from datetime import datetime
from flask import Flask, render_template, url_for
from forms import UserRegistrationForm, UserLoginForm
from flask_sqlalchemy import SQLAlchemy
from config import Config

app = Flask(__name__)  #app variable is an instance of the Flask class."__name__" is a special variable._It is just the name of the module._
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
db = SQLAlchemy(app)
app.config.from_object(Config)
Plants={
      'author': 'Username User',
      'commonName': 'Trandafir',
      'botanicalName': 'Rosa Regalis',
      'shortDescription': 'This is a beautiful plant.',
      'dateAdded': 'April 20, 2021'
    }

medicinal_use = {
    'usage':'Stress relief'
}

Dynamic_Nutrient_Accumulated={
    'N': 'True',
    'P': 'True',
    'K': 'False',
    'Ca': 'True',
    'Mg': 'True'
}
Nitrogen_Fixers_Nursing={
    'nursery': 'True',
    'check_nitrogen': 'False',
    'comment': 'This plant works best in full sunlight and requires lot of water.'
}

#Routes
@app.route("/")
@app.route("/index")   #@app is a decorator that add extra functionality to existing functions. In this case it will handle all the complicated backendstuff and allows us to write a function to view on browser.
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
@app.route("/login")
def login():
    form = UserLoginForm()
    return render_template('login.html', title= 'Login', form=form)
@app.route("/register")
def register():
    form = UserRegistrationForm()
    return render_template('register.html', title= 'Register', form=form)
@app.route("/contact")
def contact():
    return render_template('contact.html', title= 'Contact')
"""
#Creating Models for the database

#Plants Table#Users
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default = 'default.jpg')
    password = db.Column(db.String(60), nullable=False)
    add_plants = db.relationship('Plants', backref = 'author', lazy=True)

    def __repr__(self):  #How is the objected printed when we print it out. Thunder/Magic method.
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Plants(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    common_name = db.Column(db.String(40), nullable=False)
    botanical_name = db.Column(db.String(80), nullable=False)
    short_description = db.Column(db.Text, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    date_added = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    medicinal=db.relationship('Medicinal_Use', backref='plant', lazy=True )
    dna = db.relationship('Dynamic_Nutrient_Accumulated', backref='plant_dna', lazy=True)  #Dynamic_Nutrient_Accumulated
    nfn = db.relationship('Nitrogen_Fixers_Nursing', backref='plant_nfn', lazy=True)  #Nitrogen_Fixers_Nursing
    def __repr__(self):
        return f"Plants('{self.common_name}', '{self.botanical_name}', '{self.short_description} ')"

class Medicinal_Use(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usage = db.Column(db.Text, nullable=False)
    plant_id = db.Column(db.Integer, db.ForeignKey('plants.id'), nullable=False)

    def __repr__(self):
        return f"Medicinal_Use('{self.usage}', '{self.plant_id}')"


class Dynamic_Nutrient_Accumulated(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    N = db.Column(db.Boolean)
    P = db.Column(db.Boolean)
    K = db.Column(db.Boolean)
    Ca = db.Column(db.Boolean)
    S = db.Column(db.Boolean)
    Mg = db.Column(db.Boolean)
    Mn = db.Column(db.Boolean)
    Fe = db.Column(db.Boolean)
    Cu = db.Column(db.Boolean)
    Co = db.Column(db.Boolean)
    Zn = db.Column(db.Boolean)
    Si = db.Column(db.Boolean)
    plant_id = db.Column(db.Integer, db.ForeignKey('plants.id'), nullable=False)

    def __repr__(self):
        return f"Dynamic_Nutrient_Accumulated('{self.N}', '{self.P}', '{self.K}', '{self.Ca}', '{self.S}'," \
            f" '{self.Mg}', '{self.Mn}', '{self.Fe}', '{self.Cu}', '{self.Co}', '{self.Zn}', '{self.Si}', '{self.plant_id}')"

class Nitrogen_Fixers_Nursing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    check_nitrogen = db.Column(db.Boolean)
    nursery = db.Column(db.Boolean)
    comments = db.Column(db.String)
    plant_id = db.Column(db.Integer, db.ForeignKey('plants.id'), nullable=False)

    def __repr__(self):
        return f"Nitrogen_Fixers_Nursing('{self.check_nitrogen}', '{self.nursery}', '{self.plant_id}')"
"""
if __name__ == '__main__':  #The condition is true if we run the script directly.
    app.run(debug=True)