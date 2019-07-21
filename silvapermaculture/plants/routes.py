from flask import Blueprint

plants = Blueprint('plants', __name__)

#Route for users to add a plant to the database
@plants.route("/plants/new/", methods=['GET', 'POST'])
@login_required# User must be logged in to create a new plant
def new_plant():
    form = NewPlantForm()
    #Keep the default image of the plant or change it.
    if form.validate_on_submit():
        if form.plantPic.data is None:
            picture_file = "default_plant_pic.jpg"
        else:
            picture_file = save_plant_picture(form.plantPic.data)
            plant.image_file = picture_file
        new_plant = Plants(common_name = form.common_name.data, botanical_name = form.botanical_name.data,
                           short_description = form.short_description.data, medicinal=form.medicinal.data, habitats=form.habitats.data,
                           other_uses=form.other_uses.data, region=form.region.data, image_file=picture_file, author=current_user)
        for dna_element in form.dna.data:
            new_plant.dna.append(dna_element)

        for nfn_element in form.nfn.data:
            new_plant.nfn.append(nfn_element)

        db.session.add(new_plant)
        db.session.commit()
        flash(f'Thank you ! You have successfully added a plant to the database!', 'success')
        return redirect(url_for('plants'))
    image_file = url_for('static', filename='img/plants/default_plant_pic.jpg')
    return render_template('new_plant.html', title='Add new plant',
                           image_file=image_file, form=form)

#Go to specific plant with a specific ID for more information
@plants.route("/plants/<int:plant_id>")
def plant(plant_id):
    plant = Plants.query.get_or_404(plant_id)
    return render_template('plant.html', title=plant.common_name, plant=plant)


#Edit a plant with a specific ID
@plants.route("/plants/<int:plant_id>/edit", methods=['GET', 'POST'])
@login_required# User must be logged in to create a new plant
def update_plant(plant_id):
    plant = Plants.query.get_or_404(plant_id)
    #Check to see if the user who wants to update an existing plant is the actual logged user
    if plant.author != current_user:
        abort(403)
    form = UpdatePlantForm()
    #Update plant with new data from form fields
    if form.validate_on_submit():
        if form.plantPic.data:
            picture_file = save_plant_picture(form.plantPic.data)
            plant.image_file = picture_file

        plant.common_name = form.common_name.data
        plant.botanical_name = form.botanical_name.data
        plant.short_description = form.short_description.data
        plant.medicinal = form.medicinal.data
        plant.habitats = form.habitats.data
        plant.other_uses = form.other_uses.data
        plant.region = form.region.data
        plant.dna = form.dna.data
        plant.nfn = form.nfn.data
        db.session.commit()
        flash(f'You have successfully updated the plant !', 'success')

        return redirect(url_for('plant', plant_id=plant.id))
    elif request.method == 'GET':
        #Form is filled with the current data for a plant
        form.common_name.data = plant.common_name
        form.botanical_name.data = plant.botanical_name
        form.short_description.data = plant.short_description
        form.medicinal.data = plant.medicinal
        form.habitats.data = plant.habitats
        form.other_uses.data = plant.other_uses
        form.region.data = plant.region
        form.dna.data = plant.dna
        form.nfn.data = plant.nfn
    #User can go back to the plant he wanted to update, without the action of updating.
    back_to_plant = url_for('plant', plant_id=plant.id)

    image_file = url_for('static', filename='img/plants/' + plant.image_file)
    return render_template('update_plant.html', title='Update plant', image_file=image_file,
                           form=form, return_to_page=back_to_plant)

#Delete a plant with a specific ID
@plants.route("/plants/<int:plant_id>/delete", methods=['POST'])
@login_required# User must be logged in to create a new plant
def delete_plant(plant_id):
    plant = Plants.query.get_or_404(plant_id)
    # Check to see if the user who wants to update an existing plant is the actual logged user
    if plant.author != current_user:
        abort(403)
    db.session.delete(plant)
    db.session.commit()
    flash('The selected plant has been deleted!', 'success')
    return redirect(url_for('plants'))