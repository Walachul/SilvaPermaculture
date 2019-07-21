

#Function for updating default plant, scale it and use hex
def save_plant_picture(form_plantPic):
    """
    Change img filename to be a random hex, instead of keeping the original name of the file,
    in order to avoid having files with the same name.
    """
    random_hex_image = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_plantPic.filename)
    picture_fn = random_hex_image + f_ext
    picture_path = os.path.join(app.root_path, 'static/img/plants', picture_fn) #Saving the new plantPic to the specified folder.
    scale_image = (286, 180)
    img_new = Image.open(form_plantPic)
    img_new.thumbnail(scale_image)
    img_new.save(picture_path)
    return picture_fn