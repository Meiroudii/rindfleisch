from flask import Blueprint, render_template, flash, redirect
from .forms import LoginForm, SignUpForm, PasswordChangeForm
from .models import Customer
from . import db
from flask_login import login_user, login_required, logout_user, current_user
import re

auth = Blueprint('auth', __name__)


def is_valid_email(email):
    email_regex = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
    return email_regex.match(email)

def is_valid_username(username):
    username_regex = re.compile(r"^[a-zA-Z0-9_-]{3,16}$")
    return username_regex.match(username)

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    form = SignUpForm()
    if form.validate_on_submit():
        email = form.email.data
        username = form.username.data
        password1 = form.password1.data
        password2 = form.password2.data

        if not is_valid_email(email):
            flash('Invalid email address')
            return render_template('signup.html', form=form)

        if not is_valid_username(username):
            flash('Username must be 3-16 characters long and can only contain letters, numbers, underscores, and hyphens')
            return render_template('signup.html', form=form)

        if password1 != password2:
            flash('Passwords do not match')
            return render_template('signup.html', form=form)

        new_customer = Customer()
        new_customer.email = email
        new_customer.username = username
        new_customer.password = password2

        try:
            db.session.add(new_customer)
            db.session.commit()
            flash('Account Created Successfully, You can now Login')
            return redirect('/login')
        except Exception as e:
            print(e)
            flash('Account Not Created!!, Email already exists')

        form.email.data = ''
        form.username.data = ''
        form.password1.data = ''
        form.password2.data = ''

    return render_template('signup.html', form=form)
"""
@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    form = SignUpForm()
    if form.validate_on_submit():
        email = form.email.data
        username = form.username.data
        password1 = form.password1.data
        password2 = form.password2.data

        if password1 == password2:
            new_customer = Customer()
            new_customer.email = email
            new_customer.username = username
            new_customer.password = password2

            try:
                db.session.add(new_customer)
                db.session.commit()
                flash('Account Created Successfully, You can now Login')
                return redirect('/login')
            except Exception as e:
                print(e)
                flash('Account Not Created!!, Email already exists')

            form.email.data = ''
            form.username.data = ''
            form.password1.data = ''
            form.password2.data = ''

    return render_template('signup.html', form=form)
"""

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        customer = Customer.query.filter_by(email=email).first()

        if customer:
            if customer.verify_password(password=password):
                login_user(customer)
                return redirect('/')
            else:
                flash('Incorrect Email or Password')
        else:
            flash('Account does not exist, want to create an account?')
    return render_template('login.html', form=form)

@auth.route('/logout', methods=['GET', 'POST'])
@login_required
def log_out():
    logout_user()
    return redirect('/')

@auth.route('/profile/<int:customer_id>')
@login_required
def profile(customer_id):
    if current_user.id == 1 or current_user.is_admin:
        flash("Welcome Admin!!")
    customer = Customer.query.get(customer_id)
    return render_template('profile.html', customer=customer)


@auth.route('/change-password/<int:customer_id>', methods=['GET', 'POST'])
@login_required
def change_password(customer_id):
    form = PasswordChangeForm()
    customer = Customer.query.get(customer_id)
    if form.validate_on_submit():
        current_password = form.current_password.data
        new_password = form.new_password_data
        confirm_new_password = form.confirm_new_password.data

        if customer.verify_password(current_password):
            if new_password == confirm_new_password:
                customer.password = confirm_new_password
                db.session.commit()
                flash('Your password has been changed successfully')
                return redirect(f'/profile/{customer.id}')
            else:
                flash('New password does not match!!')
        else:
            flash('Current Password is incorrect')
    return render_template('change_password.html', form=form)

