#import Flask from flask
from flask import Flask
#pass current module (__name__) as argument
#this will initialize the instance
app = Flask(__name__)

# path to sqlite database
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///g4g.sqlite3"
# needed for session cookies 
app.config['SECRET_KEY'] = 'MY_SECRET'
# hashes the password and then stores in the databse
app.config['SECURITY_PASSWORD_SALT'] = "MY_SECRET"
# allows new registrations to application
app.config['SECURITY_REGISTERABLE'] = True
# to send automatic registration email to user
app.config['SECURITY_SEND_REGISTER_EMAIL'] = False

# import SQLAlchemy for database operations
# and store the instance in 'db'
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
db.init_app(app)

# runs the app instance
app.app_context().push()

from flask_security import UserMixin, RoleMixin
roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))    

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String(255), nullable=False, server_default='')
    active = db.Column(db.Boolean())
    roles = db.relationship('Role', secondary=roles_users,backref=db.backref('users', lazy='dynamic'))


class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)

@app.before_first_request
def create_tables():
    db.create_all()
    
from flask_login import LoginManager, login_manager   
from flask_security import Security, SQLAlchemySessionUserDatastore

user_datastore = SQLAlchemySessionUserDatastore(db.session, User, Role)
security = Security(app, user_datastore)

from flask import render_template
# ‘/’ URL is bound with index() function.
@app.route('/')	
#defining function index which returns the rendered html code
def index():
	return render_template("index.html")
	
from flask_security import login_required, roles_required
@app.route('/admin')
@login_required
@roles_required('admin')
def admin():
	return render_template("admin_page.html")

@app.route('/member')
@login_required
@roles_required('member')
def member():
	return render_template("member_page.html")

#for running the app
if __name__ == "__main__":  
    app.run(debug = True)
