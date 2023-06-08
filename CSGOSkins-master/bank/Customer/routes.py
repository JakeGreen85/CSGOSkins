from flask import render_template, url_for, flash, redirect, request, Blueprint
from bank import app, conn, bcrypt
from bank.forms import AddFundsForm
from flask_login import current_user, login_required
from bank.models import select_inventory, update_balance, select_balance, select_Customers


import sys, datetime

#202212
# roles is defined in the init-file
from bank import roles, mysession

iEmployee = 1
iCustomer = 2


Customer = Blueprint('Customer', __name__)


@Customer.route("/addfunds", methods=['GET', 'POST'])
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
        to_customer = form.customer.data
        amount = form.amount.data + select_balance(to_customer)
        update_balance(to_customer, amount)
        flash('Transfer succeed!', 'success')
        return redirect(url_for('Login.home'))
    return render_template('addfunds.html', title='Add Funds', form=form, role=role, balance=select_balance(current_user.get_id()))



@Customer.route("/invest", methods=['GET', 'POST'])
def invest():

    if not current_user.is_authenticated:
        flash('Please Login.','danger')
        return redirect(url_for('Login.login'))

    mysession["state"]="invest"
    print(mysession)

    role = mysession["role"]
    return render_template('invest.html', title='Invest', role=role)

@Customer.route("/inventory", methods=['GET', 'POST'])
def inventory():
    role=mysession["role"]
    inventory = select_inventory(current_user.get_id())
    return render_template('inventory.html', title="Inventory", role=role, inventory = inventory, balance=select_balance(current_user.get_id()))

@Customer.route("/account")
@login_required
def account():
    mysession["state"]="account"
    print(mysession)
    role=mysession["role"]
    return render_template('account.html', title='Account', role=role, balance=select_balance(current_user.get_id()), user=select_Customers(current_user.get_id()))