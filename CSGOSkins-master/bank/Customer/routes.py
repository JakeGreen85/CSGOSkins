from flask import render_template, url_for, flash, redirect, request, Blueprint
from bank import app, conn, bcrypt
from bank.forms import AddFundsForm
from flask_login import current_user
from bank.models import select_inventory


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
        amount = form.amount.data
        to_customer = form.customer.data
        # UpdateBalance(amount, to_customer)
        flash('Transfer succeed!', 'success')
        return redirect(url_for('Login.home'))
    return render_template('addfunds.html', title='Add Funds', form=form, role=role)



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
    return render_template('inventory.html', title="Inventory", role=role, inventory = inventory)