from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskapp.models import User
from flask_login import current_user
from flaskapp import bcrypt

class queryForm(FlaskForm):
    email = StringField('Email',validators = [DataRequired(),Email()])
    Query = StringField('Query',validators = [DataRequired(),Length(min=10,max=150)])
    submit = SubmitField('Submit')
class adminForm(FlaskForm):
    email = StringField('Email', validators = [DataRequired(),Email()])
    password = PasswordField('Password', validators = [DataRequired()])
    submit = SubmitField('Submit')

class loginForm(FlaskForm):
    email = StringField('Email', validators = [DataRequired(),Email()])
    password = PasswordField('Password', validators = [DataRequired()])
    remember = BooleanField('remember me ')
    submit = SubmitField('Submit')

class registerForm(FlaskForm):
    username = StringField('Full name', validators = [DataRequired(),Length(min=2,max=60)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    Confirmpassword = PasswordField('Confirm password', validators = [DataRequired(), EqualTo('password')])
    submit = SubmitField('Submit')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('email already present')

class updateProfile(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Update profile picture', validators = [FileAllowed(['jpg' ,'png'])])
    submit = SubmitField('Submit')

    def validate_email(self, email):
        if current_user.email != email.data:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('email already present')

class updatePassword(FlaskForm):
    oldPwd = PasswordField('Old Password', validators=[DataRequired()])
    password = PasswordField('New Password', validators=[DataRequired()])
    confirmPwd = PasswordField('Confirm password', validators=[EqualTo('password')])
    submit = SubmitField('Submit')
    def validate_oldPwd(self, oldPwd):
        if bcrypt.check_password_hash(current_user.password, oldPwd.data) == False:
            raise ValidationError('wrong password')

class uploadPicture(FlaskForm):
    picture = FileField('Update profile picture', validators = [FileAllowed(['jpg' ,'png']), DataRequired()])
    title = StringField('Title', validators = [DataRequired()])
    description = StringField('Description', validators=[])
    submit = SubmitField('Submit')
