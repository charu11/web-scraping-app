from scraping import app
import os
from flask import render_template, redirect, url_for, flash, request
from scraping import db
from scraping.forms import RegisterForm, LoginForm
from flask_login import login_user, login_required
from scraping.models import User, Details
from bs4 import BeautifulSoup
import requests
from scraping.dashboard_analysis import plotting1

url = 'https://www.sothebysrealty.be/estates/?estate_status=for-sale_en%2Cdraft-contract_en'

# home route
@app.route('/')
def home_page():
    return redirect(url_for('login_page'))

# login route
@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_user)
            return redirect(url_for('manage_data_page'))
        else:
            return redirect(url_for('login_page'))
    return render_template('login.html', form=form)

# register route
@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email=form.email.data,
                              password_hash=form.password.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f'Account created Successfully...! you are now logged in as {{ user_to_create.username }}', category='success')
        return redirect(url_for('manage_data_page'))

    if form.errors != {}:
        for error in form.errors.values():
            flash(f'There was an error with creating the user{error}', category='danger')

    return render_template('register.html', form=form)

# manage data route
@app.route('/manage_data', methods=['GET', 'POST'])
@login_required
def manage_data_page():


    if request.method == 'POST':
        # delete previous database recording beauase otherwise it will add with the new data
            del_details = Details.query.all()
            for delete in del_details:
                db.session.delete(delete)
                db.session.commit()
            # scraping
            response = requests.get(url).text
            soup = BeautifulSoup(response, 'lxml')
            tags = soup.find_all('div', class_='cnt')

            for tag in tags:

                state_name = tag.find('p', class_='city').text
                address = tag.find('p', class_='name').text
                state_address = f'{state_name}, {address}'
                state_price = tag.find('span', {'class': 'devises usd'})
                if state_price is not None:

                    details = Details(state=state_name, address=state_address, price=state_price.text[1:])
                    db.session.add(details)
                    db.session.commit()
    items = Details.query.all()
    return render_template('manage_data.html', items=items)

# dashboard route
@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard_page():
    plotting1()
    return render_template('dashboard.html')
