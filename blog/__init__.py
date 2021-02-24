from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'f67a420ab446d9111b9414d90e855c65f3b8bcd4b4d2bce4'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://c1610495:Guinness@1998@csmysql.cs.cf.ac.uk:3306/c1610495_flask_lab'

db = SQLAlchemy(app)

from flask_login import LoginManager

login_manager = LoginManager()
login_manager.init_app(app)

from blog import routes

from flask_admin import Admin 
from blog.views import AdminView
from blog.models import User, Post, Comment


admin = Admin(app, name='Admin panel', template_mode='bootstrap3') 
admin.add_view(AdminView(User, db.session)) 
admin.add_view(AdminView(Post, db.session)) 
admin.add_view(AdminView(Comment, db.session))