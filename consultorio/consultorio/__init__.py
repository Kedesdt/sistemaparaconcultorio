from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import urllib.parse


usuario = 'root'
senha= '!Q@W#E$R5t6y7u8i'
app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco_consultorio.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{}:{}@localhost/dbteste'.format(urllib.parse.quote_plus(usuario), urllib.parse.quote_plus(senha))
app.config['SECRET_KEY'] = 'chavekedes'
db  = SQLAlchemy(app)
bcrypt = Bcrypt(app)


from consultorio.controllers import rotas

