import time, datetime, pytz
from flask import render_template, session, request, redirect, url_for, Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import urllib.parse
app = Flask(__name__,template_folder="templates")
usuario = 'root'
senha= '123456'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{}:{}@localhost/Consultorio'.format(urllib.parse.quote_plus(usuario), urllib.parse.quote_plus(senha))
app.config['SECRET_KEY'] = 'chavekedes'
db  = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from consultorio.controllers import rotas

