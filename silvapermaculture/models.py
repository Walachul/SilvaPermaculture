from datetime import datetime
from silvapermaculture import db


#Models for the database


#Users
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default = 'default.png')
    add_plants = db.relationship('Plants', backref = 'author', lazy=True)

    def __repr__(self):  #How is the objected printed when we print it out. Thunder/Magic method.
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"
#Plants Table
class Plants(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    common_name = db.Column(db.String(40), nullable=False)
    botanical_name = db.Column(db.String(80), unique=True, nullable=False)
    short_description = db.Column(db.Text, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default_plant_pic.jpg')
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
