import os
import secrets
from PIL import Image
from flask import current_app


def save_picture(form_profilePic):
    """
    Change img filename to be a random hex, instead of keeping the original name of the file,
    in order to avoid having files with the same name.
    """
    random_hex_image = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_profilePic.filename)
    picture_fn = random_hex_image + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/img/profile_user', picture_fn) #Saving the new profilePic to the specified folder.
    scale_image = (125, 75)
    img_new = Image.open(form_profilePic)
    img_new.thumbnail(scale_image)
    img_new.save(picture_path)
    return picture_fn