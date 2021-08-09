from flask import Blueprint, render_template, request, redirect, url_for, flash
from marvel_app.forms import UserLoginForm, UserSignUpForm
from marvel_app.models import User, db, check_password_hash
from flask_login import login_user, logout_user, login_required

auth = Blueprint('auth', __name__, template_folder='auth_templates')

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = UserSignUpForm()
    if request.method == 'POST' and form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data

        exists = db.session.query(User.email).filter_by(email = email).first()
        if exists:
            flash(f'That email address already exists. Please sign in if that is your email address. Otherwise, sign up with a different email address.', 'signup-fail')
            return redirect(url_for('auth.signup'))
        
        new_user = User(name, email, password)
        db.session.add(new_user)
        db.session.commit()
        flash(f'New account created. Please sign in.', 'create-success')
        return redirect(url_for('auth.signin'))

    return render_template('signup.html', form = form)

@auth.route('/signin', methods=['GET', 'POST'])
def signin():
    form = UserLoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        logged_user = User.query.filter(User.email == email).first()
        if logged_user and check_password_hash(logged_user.password, password):
            login_user(logged_user)
            flash(f'Hello, {logged_user.name}', 'auth-success')
            return redirect(url_for('site.home'))
        else:
            flash(f'Incorrect email/password. Please try again.', 'auth-fail')
            return redirect(url_for('auth.signin'))
        
    return render_template('signin.html', form = form)

@auth.route('/signout')
@login_required
def signout():
    logout_user()
    flash('You have been signed out.', 'auth-success')
    return redirect(url_for('site.home'))