from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy() #Allots some space for database(Database not yet created)
DB_NAME = 'database.db' #Give name to alotted space


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'sdnfl' 
    
    #Location where we need our database to be after creation
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + path.join(path.abspath(path.dirname(__file__)), 'data.sqlite')
#     app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://zmthuexqyghuli:6e02ae4390f41339b95834758ec4db8f5e3c7853a52f71c739525312ae6708c3@ec2-3-219-135-162.compute-1.amazonaws.com:5432/d9jp99iarlhtog'
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://notesdb_3sfu_user:tdDG2ItrnqQ6Z38EV4feGiD2ujCpdAa7@dpg-cftj221a6gdotcf4g0tg-a/notesdb_3sfu'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://sam_2rpy_user:CRI9J0VVoeyqagT618wyZzR4is5Qsca3@dpg-ckgjdieafg7c73d3likg-a.oregon-postgres.render.com/sam_2rpy'


    #Tell databse that it will be accessed by app
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix = '/')
    app.register_blueprint(auth, url_prefix = '/')

    from website.models import User,Note

    create_database(app) #Function to create database

    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login' #if user is not login it will be redirect here
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
    #if database does not exist then create
    if not path.exists('website/'+ DB_NAME):
        #Create Databse
        with app.app_context():
            print(1)
#             db.init_app(app)
            print(2)
            db.create_all()
            print(3)
    print('Created Database')
