from flask import Blueprint, render_template, redirect, session, request, url_for, abort
import bcrypt
from user.models import User
from user.forms import RegisterForm, LoginForm, EditForm

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
            firstname=form.firstname.data,
            lastname=form.lastname.data
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

@user_app.route('/logout', methods=('GET', 'POST'))
def logout():
    session.pop('username')
    return redirect(url_for('user_app.login'))

@user_app.route('/<username>', methods=('GET', 'POST'))
def profile(username):
    edit_profile = False
    user = User.objects.filter(username=username).first()
    if session.get('username') and user.username == session.get('username'):
        edit_profile = True
    if user:
        return render_template('user/profile.html', user=user, edit_profile=edit_profile)
    else:
        abort(404)

@user_app.route('/edit', methods=('GET', 'POST'))
def edit():
    error = None
    message = None
    user = User.objects.filter(username=session.get('username')).first()
    if user:
        form = EditForm(obj=user)
        if form.validate_on_submit():
            if user.username != form.username.data:
                if User.objects.filter(username=form.username.data.lower()).first():
                    error = "Username already exists"
                else:
                    session['username'] = form.username.data.lower()
                    form.username.data = form.username.data.lower()
            if user.email != form.email.data:
                if User.objects.filter(email=form.email.data.lower()).first():
                    error = "Email already exists"
                else:
                    form.email.data = form.email.data.lower()
            if not error:
                form.populate_obj(user)
                user.save()
                message = "Profile updated"
        return render_template("user/edit.html", form=form, error=error, message=message)
    else:
        abort(404)
