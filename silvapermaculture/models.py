from datetime import datetime
from silvapermaculture import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#Models for the database


#Users
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default = 'default.png')
    add_plants = db.relationship('Plants', backref = 'author', lazy=True)

    def __repr__(self):  #How is the objected printed when we print it out. Dunder/Magic method.
        return f"User('{self.username}', '{self.image_file}')"
#Plants Table
class Plants(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    common_name = db.Column(db.String(40), nullable=False)
    botanical_name = db.Column(db.String(80), unique=True, nullable=False)
    short_description = db.Column(db.Text, nullable=False)
    medicinal = db.Column(db.Text, nullable=False)
    image_file = db.Column(db.String(20), default='default_plant_pic.jpg')
    date_added = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    dna_id = db.Column(db.Integer, db.ForeignKey('DNA.id'))
    dna = db.relationship('DNA', backref=db.backref('plant_dna', lazy='dynamic'))  # Dynamic_Nutrient_Accumulated
    nfn_id = db.Column(db.Integer, db.ForeignKey('NFN.id'))
    nfn = db.relationship('NFN', backref=db.backref('plant_nfn', lazy='dynamic'))  # Nitrogen_Fixers_Nursing

    def __repr__(self):
        return f"Plants('{self.common_name}', '{self.botanical_name}', '{self.short_description}'," \
            f" '{self.medicinal}', '{self.dna}', '{self.nfn}' )"

#Dynamic_Nutrient_Accumulated
class DNA(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    element = db.Column(db.String(15))

    def __repr__(self):
        return '[ {}]'.format(self.element)
#Nitrogen_Fixers_Nursing
class NFN(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    plant_extra = db.Column(db.String(40))

    def __repr__(self):
        return '[ {}]'.format(self.plant_extra)
