from flask import render_template, url_for,flash,redirect
from flaskapp.form import queryForm
from flaskapp.models import Q_form
from flaskapp import app, db

@app.route('/')
def home():
    return render_template('index.html',title="Home")

@app.route('/about')
def func():
    return render_template('about.html',title = "About")

@app.route('/contact', methods = [ 'GET' , 'POST' ])
def contact_page():
    form = queryForm()
    if form.validate_on_submit():
        response_1 = Q_form(email = form.email.data,ab = form.Query.data)
        db.session.add(response_1)
        db.session.commit()
        flash('Your response has been collected !', 'success')
        return redirect(url_for('home'))
    return  render_template('contact.html',title="Contact", form = form)