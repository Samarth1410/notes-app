#We will database models for users and notes

from website import db 
from flask_login import UserMixin
from sqlalchemy.sql import func  #func automatically gets current date time.

#Creating Blueprint of Notes DataBase
class Note(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    data = db.Column(db.String(15000000), unique = True)
    date = db.Column(db.DateTime(timezone = True), default = func.now())
    
    #To automaticaaly store ID of user from user database we used ForeignKey
    # NOTE: Although the class name is User (U capital), but the ForeignKey identifies the database by user (u small),
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) 


#Creating Blueprint of UserInfo DataBase
class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(150), unique = True)
    password = db.Column(db.String(1500))
    first_name = db.Column(db.String(15))
    #One user can have multiple notes. 
    # Therefore, a list of all the notes written by user is maintained.(Although it is not a form of list)
    notes = db.relationship('Note')


