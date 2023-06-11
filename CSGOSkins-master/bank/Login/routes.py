from flask import render_template, url_for, flash, redirect, request, Blueprint
from bank import app, conn, bcrypt
from bank.forms import LoginForm, AddCustomerForm, ChangePasswordForm, ChangeUsernameForm
from flask_login import login_user, current_user, logout_user, login_required
from bank.models import Customers, select_Customers, select_Employees, insert_Customers, select_balance, select_assets, update_password_customer, update_password_employees, update_name_customer, update_name_employees, insert_employees, insert_balance
import random

#202212
from bank import roles, mysession

Login = Blueprint('Login', __name__)

posts = [{}]


@Login.route("/")
@Login.route("/home")
def home():
    #202212
    mysession["state"]="home or /"
    print(mysession)
    #202212
    role =  mysession["role"]
    print('role: '+ role)
    all_items = select_assets()
    random_items = []
    ranint = random.randint(0, 10)
    for i in range(0, 100, 10):
        random_items.append(all_items[(ranint+i)%len(all_items)])
    if current_user.is_authenticated:  
        return render_template('home.html', posts=posts, role=role, balance=select_balance(current_user.get_id()), all_items=random_items)
    return render_template('home.html', posts=posts, role=role)


@Login.route("/about")
def about():
    #202212
    mysession["state"]="about"
    print(mysession)
    role=mysession["role"]
    if current_user.is_authenticated:  
        return render_template('about.html', title='About', role=role, balance=select_balance(current_user.get_id()))
    return render_template('about.html', title='About', role=role)


@Login.route("/login", methods=['GET', 'POST'])
def login():
    
    #202212
    mysession["state"]="login"
    print(mysession)
    role=None
    
    # jeg tror det her betyder at man er er logget på, men har redirected til login
    # så kald formen igen
    # men jeg forstår det ikke
    if current_user.is_authenticated:
        return redirect(url_for('Login.home'))    
    
    form = LoginForm()
    
    # Først bekræft, at inputtet fra formen er gyldigt... (f.eks. ikke tomt)
    if form.validate_on_submit():
        print(form.id.data)
        #"202212"
        # her checkes noget som skulle være sessionsvariable, men som er en GET-parameter
        # implementeret af AL. Ideen er at teste på om det er et employee login
        # eller om det er et customer login.
        # betinget tildeling. Enten en employee - eller en customer instantieret
        # Skal muligvis laves om. Hvad hvis nu user ikke blir instantieret
        user = select_Employees(form.id.data) if str(form.id.data).startswith('10') else select_Customers(form.id.data)
        
        # Derefter tjek om hashet af adgangskoden passer med det fra databasen...
        # Her checkes om der er logget på
        if user != None and bcrypt.check_password_hash(user.password, form.password.data):
            
            #202212
            print("role:" + user.role)
            if user.role == 'employee':  
                mysession["role"] = roles[1] #employee
            elif user.role == 'customer':  
                mysession["role"] = roles[2] #customer
            else:
                mysession["role"] = roles[0] #ingen
                
            mysession["id"] = form.id.data
            print(mysession)
            print(roles)
                            
            login_user(user, remember=form.remember.data)
            flash('Login successful.','success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('Login.home'))
        else:
            flash('Login Unsuccessful. Please check identifier and password', 'danger')

    role =  mysession["role"]
    print('role: '+ role)

    return render_template('login.html', title='Login', form=form, role=role)

@Login.route("/logout")
def logout():
    #202212
    mysession["state"]="logout"
    print(mysession)

    logout_user()
    return redirect(url_for('Login.home'))


@Login.route("/account")
@login_required
def account():
    mysession["state"]="account"
    print(mysession)
    role=mysession["role"]
    return render_template('account.html', title='Account', role=role, balance=select_balance(current_user.get_id()))

@Login.route("/market")
def market():
    if not current_user.is_authenticated:
        flash('You must be logged in to access this page', 'danger')
        return redirect(url_for('Login.home'))    
    mysession["state"]="market"
    print(mysession)      
    role=mysession["role"]
    all_items = select_assets()
    return render_template('market.html', title='Market', role=role, all_items=all_items, balance=select_balance(current_user.get_id()))

@Login.route("/createaccount", methods=['GET', 'POST'])
def createaccount():
    form = AddCustomerForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        name=form.user_name.data
        userid=form.user_id.data
        password=hashed_password
        if(str(userid).startswith('10')):
            insert_employees(userid, name, password)
        else:
            insert_Customers(userid, name, password)
        insert_balance(userid)
        flash('Account has been created! You can now login', 'success')
        return redirect(url_for('Login.home'))
    if(current_user.is_authenticated):
        return render_template('createaccount.html', title='Create Account', form=form, balance=select_balance(current_user.get_id()))
    return render_template('createaccount.html', title='Create Account', form=form)

@Login.route("/changepassword", methods=['GET', 'POST'])
@login_required
def changepassword():

    form = ChangePasswordForm()
    if form.validate_on_submit():
        if bcrypt.check_password_hash(current_user.get_password(), form.oldPassword.data):
            hashed_password = bcrypt.generate_password_hash(form.newPassword.data).decode('utf-8')
            password=hashed_password
            if(str(current_user.get_id()).startswith('10')):
                update_password_employees(current_user.get_id(), password)
            else:
                update_password_customer(current_user.get_id(), password)
            flash('Password successfully changed', 'success')
            return redirect(url_for('Login.account'))
        else:
            flash('Something went wrong', 'danger')
            return redirect(url_for('Login.home'))
    return render_template('changepassword.html', title='Change Password', form=form, balance=select_balance(current_user.get_id()))

@Login.route("/changeusername", methods=['GET', 'POST'])
@login_required
def changeusername():

    form = ChangeUsernameForm()
    if form.validate_on_submit():
        newUsername = form.user_name.data
        if(str(current_user.get_id()).startswith('10')):
            update_name_employees(current_user.get_id(), newUsername)
        else:
            update_name_customer(current_user.get_id(), newUsername)
        #UpdateUsername(user_id, newUsername)
        flash('Username successfully changed', 'success')
        return redirect(url_for('Login.account'))
    return render_template('changeusername.html', title='Change Username', form=form, balance=select_balance(current_user.get_id()))