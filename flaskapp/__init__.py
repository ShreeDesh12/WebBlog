from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__, static_folder = "static")
app.config['SECRET_KEY'] = '7dchd82hcjjs92nd'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
#app.config["SQLALchemy_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

from flaskapp import routes