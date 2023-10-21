from flask import Blueprint, render_template, redirect, url_for, request, flash
from . import db 
from .models import User
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint("auth", __name__)




@auth.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")

        if user := User.query.filter_by(email=email).first():
            if check_password_hash(user.password, password):
                flash(f"Good to have you back {user.firstname}", category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash("Incorrect password!", category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html")


@auth.route("/contact", methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
            flash('Thanks for your feedback!', category='success')
    return render_template("contact.html", current_user=current_user)



@auth.route("/sign-up", methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        firstname = request.form.get("firstname")
        lastname = request.form.get("lastname")
        email = request.form.get("email")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        if email_exists := User.query.filter_by(email=email).first():
            flash('Email already exists!', category='error')
        elif password1 != password2:
            flash('Password does not match.', category='error')
        elif len(password1) < 8:
            flash('Password is too short.', category='error')
        elif len(email) < 5:
            flash('Invalid email.', category='error')
        else:
            new_user = User(firstname=firstname, lastname=lastname, email=email, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash('Account created!')
            login_user(new_user, remember=True)

            return redirect(url_for('views.home'))


    return render_template("signup.html")


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!', category='success')
    return redirect(url_for("views.home"))