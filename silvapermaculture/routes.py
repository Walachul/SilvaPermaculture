import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from silvapermaculture import app, db, bcrypt
from silvapermaculture.forms import UserRegistrationForm, UserLoginForm, UpdateAccountForm,\
    NewPlantForm, UpdatePlantForm, SearchForm, SearchFormN
from silvapermaculture.models import User, Plants
from flask_login import login_user, current_user, logout_user, login_required





