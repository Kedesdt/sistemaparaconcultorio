import time, datetime, pytz
from flask import render_template, session, request, redirect, url_for, Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename
from os.path import join, dirname, realpath
import urllib.parse
app = Flask(__name__,template_folder="templates")
usuario = 'root'
senha= '!Q@W#E$R5t6y7u8i'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg','bmp'}
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{}:{}@diastorres.com/banco'.format(urllib.parse.quote_plus(usuario), urllib.parse.quote_plus(senha))
app.config['SECRET_KEY'] = 'chavekedes'
db  = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from consultorio.controllers import rotas

