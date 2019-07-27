from silvapermaculture import create_app, db
from silvapermaculture.models import DNA, NFN
app = create_app()

with app.app_context():
    db.create_all()
    element1 = DNA(element="Nitrogen")
    element2 = DNA(element="Phosphorus")
    element3 = DNA(element="Potassium")
    element4 = DNA(element="Calcium")
    element5 = DNA(element="Sulfur")
    element6 = DNA(element="Magnesium")
    element7 = DNA(element="Manganese")
    element8 = DNA(element="Iron")
    element9 = DNA(element="Copper")
    element10 = DNA(element="Cobalt")
    element11 = DNA(element="Zinc")
    element12 = DNA(element="Silicon")
    extra1 = NFN(plant_extra="Nitrogen Fixator")
    extra2 = NFN(plant_extra="Nurse Plant")
    db.session.add_all([element1, element2, element3, element4, element5, element6,
                        element7, element8, element9, element10, element11,
                        element12, extra1, extra2])
    db.session.commit()

if __name__ == '__main__':  #The condition is true if we run the script directly.
    app.run(debug=False)
