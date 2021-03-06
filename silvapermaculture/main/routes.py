from flask import render_template, request,Blueprint
from silvapermaculture.models import Plants
from silvapermaculture.plants.forms import SearchForm,SearchFormN
main = Blueprint('main', __name__)


#Routes
@main.route("/")
@main.route("/index")
def index():
    return render_template('index.html')
@main.route("/plants")
def plants():
    page = request.args.get('page', 1, type=int)
    plants = Plants.query.order_by(Plants.date_added.desc()).paginate(page=page, per_page=6)
    search = SearchForm()
    searchn = SearchFormN()

    return render_template('plants.html', title='Plants Database', plants=plants, search=search, searchn=searchn)