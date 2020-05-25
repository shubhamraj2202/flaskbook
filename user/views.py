from flask import Blueprint, render_template, redirect, session, request
import bcrypt
from user.models import User
from user.forms import RegisterForm, LoginForm

user_app = Blueprint('user_app', __name__) # To call this module

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

@user_app.route('/login', methods=('GET', 'POST'))
def login():
    form = LoginForm()
    error = None

    if request.method == 'GET' and request.args.get('next'):
        session['next'] = request.args.get('next')

    if form.validate_on_submit():
        user = User.objects.filter(username=form.username.data).first()
        if user:
            user_password = user.password.encode('utf-8')
            if bcrypt.hashpw(form.password.data.encode('utf-8'), user_password) == user_password:
                session['username'] = form.username.data
                if 'next' in session:
                    next = session.get('next')
                    session.pop('next')
                    return redirect(next)
                else:
                    return 'User Logged In'
            else:
                user = None
        if not user:
            error = 'Incorrect Credentials'
    return render_template('user/login.html', form=form, error=error)
