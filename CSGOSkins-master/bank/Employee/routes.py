from flask import render_template, url_for, flash, redirect, request, Blueprint
from bank import app, conn, bcrypt
from bank.forms import AddCustomerForm
from bank.forms import AddFundsForm
from flask_login import current_user
from bank.models import Transfers, CheckingAccount, InvestmentAccount,  transfer_account, insert_Customers, update_CheckingAccount
import sys, datetime

#202212
from bank import roles, mysession
from bank.models_e import select_emp_investments_with_certificates, select_emp_investments, select_emp_investments_certificates_sum


iEmployee = 1
iCustomer = 2 # bruges til transfer/

Employee = Blueprint('Employee', __name__)

@Employee.route("/createaccount", methods=['GET', 'POST'])
def addcustomer():
    
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
        CPR_number=form.CPR_number.data
        password=hashed_password
        insert_Customers(name, CPR_number, password)
        flash('Account has been created! You can now login', 'success')
        return redirect(url_for('Login.home'))
    return render_template('createaccount.html', title='Create Account', form=form)

@Employee.route("/inventory", methods=['GET', 'POST'])
def inventory():
    role=mysession["role"]
    return render_template('inventory.html', title="Inventory", role=role)

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
        date = datetime.date.today()
        amount = form.amount.data
        to_customer = form.customer.data
        update_CheckingAccount(amount, to_customer)
        flash('Transfer succeed!', 'success')
        return redirect(url_for('Login.home'))
    return render_template('addfunds.html', title='Add Funds', form=form, role=role)