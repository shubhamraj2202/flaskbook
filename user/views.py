from flask import Blueprint, render_template
import bcrypt
from user.models import User
from user.forms import RegisterForm

user_app = Blueprint('user_app', __name__) # To call this module

@user_app.route('/login')
def login():
    return "User Login"

@user_app.route('/register', methods=('GET', 'POST'))
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(form.password.data.encode('utf-8'), salt)
        user = User(
            username=form.username.data,
            password=hashed_password,
            email=form.email.data,
            firstname=form.first_name.data,
            lastname=form.last_name.data
            )
        user.save()
        return "User registered"

    return render_template('user/register.html', form=form)
