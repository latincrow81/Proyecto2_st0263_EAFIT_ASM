from flask import Blueprint, url_for, redirect
from flask_login import login_user, logout_user, login_required
from flask import request, flash, render_template
from app.db_api import DbAPI
from .models import User
from .forms import LoginForm, RegistrationForm

auth_blueprint = Blueprint('auth', __name__)

db_api = DbAPI()


@auth_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if form.validate_on_submit():
        with db_api.session_local() as session:
            user = User(username=form.username.data,
                        email=form.email.data,
                        password=form.password.data)
            user.activated = True
            session.add(user)
            session.commit()
            login_user(user)
            flash('Registration successful. You are logged in.', 'success')
            return redirect(url_for("main.index"))
    elif form.is_submitted():
        flash('The given data was invalid.', 'danger')
    return render_template('auth/register.html', form=form)


@login_required
@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.authenticate(form.user_id.data, form.password.data)
        if user is not None:
            login_user(user)
            flash('Login successful.', 'success')
            return redirect(url_for('main.index'))
        flash('Wrong user ID or password.', 'danger')
    return render_template('auth/login.html', form=form)


@auth_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You were logged out.', 'info')
    return redirect(url_for('main.index'))
