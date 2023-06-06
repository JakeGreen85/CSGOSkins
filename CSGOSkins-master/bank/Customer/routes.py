from flask import render_template, url_for, flash, redirect, request, Blueprint
from bank import app, conn, bcrypt
from bank.forms import DepositForm, InvestForm
from bank.forms import TransferForm
from flask_login import current_user
from bank.models import CheckingAccount, InvestmentAccount, update_CheckingAccount
from bank.models import select_cus_investments_with_certificates, select_cus_investments, select_cus_investments_certificates_sum
from bank.models import select_cus_accounts,  transfer_account


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

    # CUS7 is the customer transfer. Create new endpoint.
    # EUS10 is the employee transfer.
    # manageCustor/ er EUS!=
    # transfer/  må være CUS7
    # move to customer DONE
    # duplicate back and change database access here


    if not mysession["role"] == roles[iCustomer]:
        flash('transfer money customer mode.','danger')
        return redirect(url_for('Login.login'))


    CPR_number = current_user.get_id()
    print(CPR_number)
    dropdown_accounts = select_cus_accounts(current_user.get_id())
    drp_accounts = []
    for drp in dropdown_accounts:
        drp_accounts.append((drp[3], drp[1]+' '+str(drp[3])))
    print(drp_accounts)
    form = TransferForm()
    form.sourceAccount.choices = drp_accounts
    form.targetAccount.choices = drp_accounts
    role=mysession["role"]
    if form.validate_on_submit():
        date = datetime.date.today()
        amount = form.amount.data
        from_account = form.sourceAccount.data
        to_account = form.targetAccount.data
        transfer_account(date, amount, from_account, to_account)
        flash('Transfer succeed!', 'success')
        return redirect(url_for('Login.home'))
    return render_template('transfer.html', title='Transfer', drop_cus_acc=dropdown_accounts, form=form, role=role)



@Customer.route("/invest", methods=['GET', 'POST'])
def invest():

    if not current_user.is_authenticated:
        flash('Please Login.','danger')
        return redirect(url_for('Login.login'))

    mysession["state"]="inventory"
    print(mysession)

    role = mysession["role"]
    return render_template('inventory.html', title='Inventory', role=role)


@Customer.route("/deposit", methods=['GET', 'POST'])
def deposit():
    if not current_user.is_authenticated:
        flash('Please Login.','danger')
        return redirect(url_for('Login.login'))


    #202212
    #EUS-CUS10
    # move to employee object
    if not mysession["role"] == roles[iEmployee]:
        flash('Deposit is employee only.','danger')
        return redirect(url_for('Login.login'))

    mysession["state"]="deposit"
    print(mysession)


    form = DepositForm()
    if form.validate_on_submit():
        amount=form.amount.data
        CPR_number = form.CPR_number.data
        update_CheckingAccount(amount, CPR_number)
        flash('Succeed!', 'success')
        return redirect(url_for('Login.home'))
    return render_template('deposit.html', title='Deposit', form=form)

@Customer.route("/summary", methods=['GET', 'POST'])
def summary():
    if not current_user.is_authenticated:
        flash('Please Login.','danger')
        return redirect(url_for('Login.login'))
    if form.validate_on_submit():
        pass
        flash('Succeed!', 'success')
        return redirect(url_for('Login.home'))
    return render_template('deposit.html', title='Deposit', form=form)

@Customer.route("/inventory", methods=['GET', 'POST'])
def inventory():
    role=mysession["role"]
    return render_template('inventory.html', title="Inventory", role=role)