from flask import Blueprint,render_template,request, flash, redirect, url_for
from website.models import User
from werkzeug.security import generate_password_hash, check_password_hash
from website import db
from flask_login import login_user, login_required, logout_user, current_user, LoginManager

auth = Blueprint('auth',__name__)

@auth.route('/login', methods=['GET','POST'])
def login():
    #request has all the imformation about form,post,get,methods etc
    # data = request.form
    # print(data)

    #If we are sending post request i.e. loggingin
    if request.method == 'POST':
        #Inputs given by user
        email = request.form.get('email')
        password = request.form.get('password')

        #Checking in database
        user = User.query.filter_by(email = email).first()
        if user: #If user exist
            if check_password_hash(user.password, password):
                flash("Login Successful", category="success")
                login_user(user, remember =True) #It will remember the user until the session expire
                return redirect(url_for('views.home'))
            else:
                flash("Incorrect Passowrd!", category="error")
        else:
            flash("Email Not registered", category="error")   

    return render_template('login.html', user = current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods = ['GET','POST'])
def sign_up():
    if request.method == 'POST':
        #use .get for specific attribute 'name' in html
        email = request.form.get('email')
        firstname = request.form.get('firstname')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email = email).first()
        if user:
            flash('Email already exists', category="error")

        elif len(email)<4:
            flash('Email must be greater than 4 characters', category='error') #catrogy to display color
        elif len(firstname)<2:
            flash('First Name must be greater than 1 characters', category='error')
        elif len(password1)<7:
            flash('Passsword must be greater than 6 characters', category='error')
        elif password1!=password2:
            flash('Password don\'t match', category='error')
        else:
            new_user = User(email= email, first_name = firstname, password = generate_password_hash(password1, method = 'sha256'))
            # print(new_user)
            db.session.add(new_user)
            db.session.commit()
            # login_user(user, remember =True) #Session will remeber the user
            flash('Account Created', category='success') #catrogy to display color
            return redirect(url_for('views.home'))

        #NOTE: to display flash messages we need to write some code in base.html

    return render_template('sign_up.html', user = current_user)
