from flask import render_template, url_for, flash, redirect, request, Blueprint
from bank import app, conn, bcrypt
from bank.forms import AddCustomerForm
from bank.forms import AddFundsForm
from flask_login import current_user, login_required
from bank.models import insert_Customers, update_balance, select_balance, select_Employees
import sys, datetime

#202212
from bank import roles, mysession


iEmployee = 1
iCustomer = 2 # bruges til transfer/

Employee = Blueprint('Employee', __name__)

@Employee.route("/createaccount", methods=['GET', 'POST'])
def createaccount():
    
    if not current_user.is_authenticated:
        return redirect(url_for('Login.home'))
        
    #202212
    # employee only
    if not mysession["role"] == roles[iEmployee]:  
        flash('Adding customers is employee only.','danger')
        return redirect(url_for('Login.login'))

    form = AddCustomerForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        name=form.username.data
        userid=form.userid.data
        password=hashed_password
        insert_Customers(name, userid, password)
        flash('Account has been created! You can now login', 'success')
        return redirect(url_for('Login.home'))
    return render_template('createaccount.html', title='Create Account', form=form)

@Employee.route("/inventory", methods=['GET', 'POST'])
def inventory():
    role=mysession["role"]
    return render_template('inventory.html', title="Inventory", role=role, balance=select_balance(current_user.get_id()))

@Employee.route("/addfunds", methods=['GET', 'POST'])
def addfunds():
    if not current_user.is_authenticated:
        flash('Please Login.','danger')
        return redirect(url_for('Login.login'))

    if not mysession["role"] == roles[iEmployee]:
        flash('Only employees can add funds','danger')
        return redirect(url_for('Login.login'))

    form = AddFundsForm()
    role=mysession["role"]
    if form.validate_on_submit():
        to_customer = form.customer.data
        amount = form.amount.data + select_balance(to_customer)
        update_balance(to_customer, amount)
        flash('Transfer succeed!', 'success')
        return redirect(url_for('Login.home'))
    return render_template('addfunds.html', title='Add Funds', form=form, role=role, balance=select_balance(current_user.get_id()))

@Employee.route("/account")
@login_required
def account():
    mysession["state"]="account"
    print(mysession)
    role=mysession["role"]
    return render_template('account.html', title='Account', role=role, balance=select_balance(current_user.get_id()), user=select_Employees(current_user.get_id()))