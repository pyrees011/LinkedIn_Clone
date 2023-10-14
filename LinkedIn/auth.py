from flask import Blueprint, redirect, render_template, url_for, current_app, flash
from .model import SignupForm, LoginForm
from .sqlite import insertDataIntoUsers, authenticate, getUsername
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from .model import User

auth = Blueprint("auth", __name__)


@auth.route('/signup', methods=['GET', 'POST'])
def sign_up():
    form = SignupForm()

    if form.validate_on_submit():

        username = form.username.data
        email = form.email.data
        password = form.password.data
        pro_type = form.pro_type.data

        hash_password = generate_password_hash(password)

        insertDataIntoUsers(username, email, hash_password, pro_type)
        return redirect(url_for('views.homepage'))
        
    return render_template('signup.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if current_user.is_authenticated:
        return redirect(url_for('views.homepage'))

    if form.validate_on_submit():

        username = form.username.data
        password = form.password.data

        data = authenticate(username)
        if data:
            if check_password_hash(data[2], password):
                user = User(id=data[0], username=data[1], password=data[2], email=data[3], type=data[4])
                login_user(user)
                flash("Successfully logged In", category="success")
                return redirect(url_for('views.homepage'))
            else:
                flash("Login Failed! check your password", category="error")
                return redirect(url_for('auth.login'))
        else:
            flash("Email does not exists! create an account", category="error")
            return redirect(url_for('auth.login'))

    return render_template('login.html', form=form)


@auth.route('/employer_login')
def employer_login():
    form = LoginForm()
    return render_template('employer_login.html', form=form)

@auth.route('/employer_signUp')
def employer_signUp():
    form = SignupForm()
    return render_template('employer_signUp.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))