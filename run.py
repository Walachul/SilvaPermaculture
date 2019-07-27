from silvapermaculture import create_app, db
from silvapermaculture.models import Dna, Nfn
app = create_app()

with app.app_context():
    db.create_all()
    element1 = Dna(element="Nitrogen")
    element2 = Dna(element="Phosphorus")
    element3 = Dna(element="Potassium")
    element4 = Dna(element="Calcium")
    element5 = Dna(element="Sulfur")
    element6 = Dna(element="Magnesium")
    element7 = Dna(element="Manganese")
    element8 = Dna(element="Iron")
    element9 = Dna(element="Copper")
    element10 = Dna(element="Cobalt")
    element11 = Dna(element="Zinc")
    element12 = Dna(element="Silicon")
    extra1 = Nfn(plant_extra="Nitrogen Fixator")
    extra2 = Nfn(plant_extra="Nurse Plant")
    db.session.add_all([element1, element2, element3, element4, element5, element6,
                        element7, element8, element9, element10, element11,
                        element12, extra1, extra2])
    db.session.commit()

if __name__ == '__main__':  #The condition is true if we run the script directly.
    app.run(debug=False)
