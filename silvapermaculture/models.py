from datetime import datetime
from silvapermaculture import db, login_manager
from flask_login import UserMixin
from silvapermaculture.search import add_element_index, remove_element_from_index, search_index



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#Models for the database


#Users
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    image_file = db.Column(db.String(100), nullable=False, default = 'default.png')
    add_plants = db.relationship('Plants', backref = 'author', lazy=True)

    def __repr__(self):  #How is the objected printed when we print it out. Dunder/Magic method.
        return f"User('{self.username}', '{self.image_file}')"

plants_dna_table = db.Table(
    'plants_dna',
    db.Column('plants_id', db.Integer, db.ForeignKey('plants.id'), nullable=False),
    db.Column('dna_id', db.Integer, db.ForeignKey('DNA.id'), nullable=False),
    db.UniqueConstraint('plants_id', 'dna_id')
)
plants_nfn_table = db.Table(
    'plants_nfn',
    db.Column('plants_id', db.Integer, db.ForeignKey('plants.id'), nullable=False),
    db.Column('nfn_id', db.Integer, db.ForeignKey('NFN.id'), nullable=False),
    db.UniqueConstraint('plants_id', 'nfn_id')
)

#Mixin class that creates bondage between Elasticsearch and SQLAlchemy.
# Updates on the SQLAlchemy session are applied also to Elasticsearch index, when attached as subclass to a model.
class SearchitMixin(object):
    #search function that replaces object ID from the query with objects.
    @classmethod
    def search(cls, expression, page, per_page):
        ids, total = search_index(cls.__tablename__, expression, page, per_page)
        if total == 0:
            return cls.query.filter_by(id=0), 0
        when = []
        for i in range(len(ids)):
            when.append((ids[i],i))
        #case statement to ensure that the results from the database come in same order as ids are given.
        return cls.query.filter(cls.id.in_(ids)).order_by(
            db.case(when, value=cls.id)), total
    #Corresponds to SQLAlchemy event before committing the session and save the objects.
    @classmethod
    def before_commit(cls,session):
        session._changes={
            'add': list(session.new),
            'update': list(session.dirty),
            'delete': list(session.deleted)
        }
    #The session was committed and now we can iterate over the saved objects with Elasticsearch
    @classmethod
    def after_commit(cls,session):
        for obj in session._changes['add']:
            if isinstance(obj, SearchitMixin):
                add_element_index(obj.__tablename__, obj)
        for obj in session._changes['update']:
            if isinstance(obj, SearchitMixin):
                add_element_index(obj.__tablename__, obj)
        for obj in session._changes['delete']:
            if isinstance(obj, SearchitMixin):
                remove_element_from_index(obj.__tablename__, obj)
        session._changes = None
    #Helper to refresh an elasticsearch index with all the data from the SQLite database.
    @classmethod
    def reindex(cls):
        for obj in cls.query:
            add_element_index(cls.__tablename__, obj)
db.event.listen(db.session, 'before_commit', SearchitMixin.before_commit)
db.event.listen(db.session, 'after_commit', SearchitMixin.after_commit)

#Plants Table
class Plants(SearchitMixin, db.Model):
    __searchit__ = ['common_name', 'botanical_name', 'medicinal', 'region']
    id = db.Column(db.Integer, primary_key=True)
    common_name = db.Column(db.String(40), nullable=False)
    botanical_name = db.Column(db.String(80), unique=True, nullable=False)
    short_description = db.Column(db.Text, nullable=False)
    medicinal = db.Column(db.Text, nullable=False)
    other_uses = db.Column(db.Text, nullable=False)
    habitats = db.Column(db.Text, nullable=False)
    region = db.Column(db.Text, nullable=False)
    image_file = db.Column(db.String(100), default='default_plant_pic.jpg')
    date_added = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    dna = db.relationship('DNA', secondary = plants_dna_table)  # Dynamic_Nutrient_Accumulated
    nfn = db.relationship('NFN', secondary = plants_nfn_table)  # Nitrogen_Fixers_Nursing

    def __repr__(self):
        return f"Plants('{self.common_name}', '{self.botanical_name}', '{self.short_description}'," \
            f" '{self.medicinal}', '{self.dna}', '{self.nfn}' )"

#Dynamic_Nutrient_Accumulated
class DNA(SearchitMixin, db.Model):
    __searchit__ = ['element']
    id = db.Column(db.Integer, primary_key=True)
    element = db.Column(db.String(15))

    def __repr__(self):
        return '{}'.format(self.element)
#Nitrogen_Fixers_Nursing
class NFN(SearchitMixin, db.Model):
    __searchit__ = ['plant_extra']
    id = db.Column(db.Integer, primary_key=True)
    plant_extra = db.Column(db.String(40))

    def __repr__(self):
        return '{}'.format(self.plant_extra)
