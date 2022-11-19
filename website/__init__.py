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
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

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
            db.init_app(app)
            db.create_all()
    print('Created Database')
