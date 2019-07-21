import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from silvapermaculture import app, db, bcrypt
from silvapermaculture.forms import UserRegistrationForm, UserLoginForm, UpdateAccountForm,\
    NewPlantForm, UpdatePlantForm, SearchForm, SearchFormN
from silvapermaculture.models import User, Plants
from flask_login import login_user, current_user, logout_user, login_required

#Routes
@app.route("/")
@app.route("/index")
def index():
    return render_template('index.html')
@app.route("/plants")
def plants():
    page = request.args.get('page', 1, type=int)
    plants = Plants.query.order_by(Plants.date_added.desc()).paginate(page=page, per_page=5)
    search = SearchForm()
    searchn = SearchFormN()

    return render_template('plants.html', title= 'Plants Database', plants=plants, search=search, searchn=searchn)
@app.route("/statistics")
def statistics():
    return render_template('statistics.html', title= 'Statistics')



#Implementing Search
@app.route("/search")
def search():
    search = SearchForm()
    #Doesn't check the data, just if the fields are empty raises an error
    if not search.validate():
        return redirect(url_for('plants'))
    page = request.args.get('page', 1, type=int)
    plants, total = Plants.search(search.q.data, page,
                                  app.config['PLANTS_PER_PAGE'])
    next_url = url_for('search', q=search.q.data, page=page + 1) \
        if total > page * app.config['PLANTS_PER_PAGE'] else None
    prev_url = url_for('search', q=search.q.data, page=page - 1) \
        if page > 1 else None

    return render_template('results.html', title="Search results", search=search,
                           total=total, plants=plants, next_url=next_url, prev_url=prev_url)

#Search based on filters
@app.route("/searchn")
def searchn():
    searchn = SearchFormN()
    if not searchn.validate():
        return redirect(url_for('plants'))
    if searchn.dna.data:
        for e in searchn.dna.data:
            filterQuery = Plants.query.join('dna').filter_by(element=str(e)).all()
    elif searchn.nfn.data:
        for d in searchn.nfn.data:
            filterQuery = Plants.query.join('nfn').filter_by(plant_extra=str(d)).all()

    return render_template('search_filter.html', title="Filtered search results", searchn=searchn,
                                       filterQuery=filterQuery)
