from flask import render_template, url_for,flash,redirect , request
from flaskapp.form import queryForm, adminForm, loginForm, registerForm, updateProfile, updatePassword, uploadPicture
from flaskapp.models import Q_form, User, post
from flaskapp import app, db, login_manager, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
import secrets
import os
from PIL  import Image
from sqlalchemy import desc


@app.route('/')
def home():
    return render_template('index.html',title="Home",  query= post.query.order_by(desc(post.id)).all())

@app.route('/about')
def func():
    return render_template('about.html',title = "About")
    
@app.route('/timeline')
def timeline():
    return render_template('timeline.html',title = "Timeline")

@app.route('/contact', methods = [ 'GET' , 'POST' ])
def contact_page():
    form = queryForm()
    image_file = 'default.jpg'
    if current_user.is_authenticated:
        image_file = ('profile_pics/' + current_user.picture)
    if form.validate_on_submit():
        response_1 = Q_form(email = form.email.data,ab = form.Query.data)
        db.session.add(response_1)
        db.session.commit()
        flash('Your response has been collected !', 'success')
        return redirect(url_for('home'))
    elif request.method == 'GET' and current_user.is_authenticated:
        form.email.data = current_user.email
    return  render_template('contact.html',title="Contact", form = form,image_file= image_file)

@app.route('/adminLogin', methods = [ 'GET' , 'POST' ])
def check_admin():
    form = adminForm()
    if current_user.is_authenticated:
        return redirect(url_for('admin'))
    if form.validate_on_submit():
        if(form.email.data == 'shree.desh72@gmail.com' and form.password.data == 'shree123'):
            return render_template('admin.html', title="Admin-Page", query=Q_form.query.all())
        else:
            flash('Wrong Id or password', 'danger')
    return render_template('adminLogin.html',title = "login", form = form)

@app.route('/register', methods = ['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = registerForm()
    if form.validate_on_submit():
        hashPassword = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username = form.username.data , email = form.email.data, password = hashPassword)
        if(user.email == User.query.filter_by(email = user.email).first()):
            flash('Email already exist', 'danger')
            return redirect(url_for('login'))
        db.session.add(user)
        db.session.commit()
        flash('Account has been created', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title = 'Sign up', form = form)


@app.route('/login', methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = loginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email= form.email.data).first()
        if user and (bcrypt.check_password_hash(user.password, form.password.data)):
            login_user(user, remember=form.remember.data)
            flash('Successfully logged in !', 'success')
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            return redirect(url_for('home'))
        else:
            flash('Incorrect username or password', 'danger')
    return render_template('login.html', title = 'Login', form = form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

def savepicture(form_pic, opSize, folder='profile_pics'):
    _, ext= os.path.splitext(form_pic.filename)
    pic = secrets.token_hex(8)
    picName = pic + ext
    picPath = os.path.join(app.root_path , 'static/'+folder , picName)
    i = Image.open(form_pic)
    i.thumbnail(opSize)
    i.save(picPath)
    return picName

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = updateProfile()
    if form.validate_on_submit():
        if form.picture.data:
            img_file = savepicture(form.picture.data, opSize= (100,100))
            current_user.picture = img_file
        current_user.email = form.email.data
        db.session.commit()
        flash('Successfully updated', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.picture)
    return render_template('account.html', title = 'account', form = form, image_file= image_file)

@app.route('/change-password',methods=['GET', 'POST'])
@login_required
def changepwd():
    form = updatePassword()
    if form.validate_on_submit():
        hashPwd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        current_user.password = hashPwd
        db.session.commit()
        flash('Password updated', 'success')
    image_file = ('profile_pics/' + current_user.picture)
    return render_template('changepwd.html', title= 'Change Password', form = form, image_file=image_file)

@app.route('/upload-picture', methods=['GET', 'POST'])
@login_required
def upload_pic():
    form = uploadPicture()
    if form.validate_on_submit():
        img_file = savepicture(form.picture.data, opSize=(300,300), folder='post')
        p = post(picture = img_file, title = form.title.data, author = current_user.username, postedBy = current_user.id)
        if form.description.data:
            p.description = form.description.data
        db.session.add(p)
        db.session.commit()
        return  redirect(url_for('home'))
        flash('Successfully uploaded', 'info')
    image_file = url_for('static', filename='profile_pics/' + current_user.picture)
    return render_template('uploadPicture.html', title='Upload Picture', form = form, image_file = image_file)
