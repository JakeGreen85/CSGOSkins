# write all your SQL queries in this file.
from datetime import datetime
from bank import conn, login_manager
from flask_login import UserMixin
from psycopg2 import sql

@login_manager.user_loader
def load_user(user_id):
    cur = conn.cursor()

    schema = 'customers'
    id = 'user_id'
    if str(user_id).startswith('10'):
        schema = 'employees'
        id = 'user_id'

    user_sql = sql.SQL("""
    SELECT * FROM {}
    WHERE {} = %s
    """).format(sql.Identifier(schema),  sql.Identifier(id))

    cur.execute(user_sql, (int(user_id),))
    if cur.rowcount > 0:
        # return-if svarer til nedenstående:
    		# if schema == 'employees':
    		#   return Employees(cur.fetchone())
    		# else:
    		#   return Customers(cur.fetchone())

        return Employees(cur.fetchone()) if schema == 'employees' else Customers(cur.fetchone())
    else:
        return None
    

class Asset(tuple, UserMixin):
    def __init__(self, user_data):
        self.classid = user_data[0]
        self.instanceid = user_data[1]
        self.name = user_data[2]
        self.price = user_data[3]
        self.icon_url = user_data[4]
        self.quality = user_data[5]
    def get_id(self):
        return (self.classid, self.instanceid)


class Customers(tuple, UserMixin):
    def __init__(self, user_data):
        self.userid = user_data[0]
        self.password = user_data[1]
        self.name = user_data[2]
        self.role = "customer"

    def get_id(self):
       return (self.userid)
    
    def get_password(self):
        return (self.password)

class Employees(tuple, UserMixin):
    def __init__(self, employee_data):
        self.id = employee_data[0]
        self.name = employee_data[1]
        self.password = employee_data[2]
        self.role = "employee"

    def get_id(self):
       return (self.id)

class CheckingAccount(tuple):
    def __init__(self, user_data):
        self.id = user_data[0]
        self.create_date = user_data[1]
        self.userid = user_data[2]
        self.amount = 0

class InvestmentAccount(tuple):
    def __init__(self, user_data):
        self.id = user_data[0]
        self.start_date = user_data[1]
        self.maturity_date = user_data[2]
        self.amount = 0

class Transfers(tuple):
    def __init__(self, user_data):
        self.id = user_data[0]
        self.amount = user_data[1]
        self.transfer_date = user_data[2]
        
def create_tables():
    cur = conn.cursor()
    sql = """
        CREATE TABLE IF NOT EXISTS assets (
            classid bigint,
            instanceid bigint,
            name varchar,
            price int,
            quality varchar,
            icon_url varchar,
            PRIMARY KEY (classid, instanceid));
    """
    cur.execute(sql)
    conn.commit()
    cur.close()
    
def insert_asset(classid, instanceid, name, price, quality, icon_url):
    cur = conn.cursor()
    sql = """
    INSERT INTO assets(classid, instanceid, name, price, quality, icon_url)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    cur.execute(sql, (classid, instanceid, name, price, quality, icon_url))
    conn.commit()
    cur.close()
    
def get_assets_of_quality(quality):
    cur = conn.cursor()
    sql = """
    SELECT * FROM assets
    WHERE quality = %s
    """
    cur.execute(sql, (quality,))
    
    items = []
    for asset in cur.fetchall():
        items.append(Asset(asset)) 
    cur.close()
    return items
    

def insert_Customers(userid, name, password):
    cur = conn.cursor()
    sql = """
    INSERT INTO Customers(User_id, name, password)
    VALUES (%s, %s, %s)
    """
    cur.execute(sql, (userid, name, password))
    # Husk commit() for INSERT og UPDATE, men ikke til SELECT!
    conn.commit()
    cur.close()

def insert_employees(userid, name, password):
    cur = conn.cursor()
    sql = """
    INSERT INTO Employees(User_id, name, password)
    VALUES (%s, %s, %s)
    """
    cur.execute(sql, (userid, name, password))
    conn.commit()
    cur.close()
    
def select_assets():
    cur = conn.cursor()
    sql = """
    SELECT * FROM assets
    """
    cur.execute(sql)
    items = []
    for asset in cur.fetchall():
        items.append(Asset(asset)) 
    cur.close()
    return items

def select_Customers(userID):
    print("customer")
    cur = conn.cursor()
    sql = """
    SELECT * FROM Customers
    WHERE User_id = %s
    """
    cur.execute(sql, (userID,))
    user = Customers(cur.fetchone()) if cur.rowcount > 0 else None;
    cur.close()
    return user

def select_Employees(userID):
    print("employee")
    cur = conn.cursor()
    sql = """
    SELECT * FROM Employees
    WHERE User_id = %s
    """
    cur.execute(sql, (userID,))
    user = Employees(cur.fetchone()) if cur.rowcount > 0 else None;
    cur.close()
    return user

def update_CheckingAccount(amount, userid):
    cur = conn.cursor()
    sql = """
    UPDATE CheckingAccount
    SET amount = %s
    WHERE userid = %s
    """ 
    cur.execute(sql, (amount, userid))
    # Husk commit() for INSERT og UPDATE, men ikke til SELECT!
    conn.commit()
    cur.close()

def select_CheckingAccount(userid):
    cur = conn.cursor()
    sql = """
    SELECT CheckingAccount
    WHERE userid = %s
    """
    cur.execute(sql, (userid))
    cur.close()
    
def transfer_account(date, amount, from_account, to_account):
    cur = conn.cursor()
    sql = """
    INSERT INTO Transfers(transfer_date, amount, from_account, to_account)
    VALUES (%s, %s, %s, %s)
    """
    cur.execute(sql, (date, amount, from_account, to_account))
    # Husk commit() for INSERT og UPDATE, men ikke til SELECT!
    conn.commit()
    cur.close()
    
def select_inventory(user_id):
    cur = conn.cursor()
    sql = """
    SELECT assets.* FROM assets, inventory
    WHERE inventory.user_id = %s
    AND assets.classid = inventory.classid
    AND assets.instanceid = inventory.instanceid
    """
    
    cur.execute(sql, (user_id,))
    inventory = []
    for asset in cur.fetchall():
        inventory.append(Asset(asset)) 
    cur.close()
    return inventory

def update_password_customer(user_id, new_password):
    cur = conn.cursor()
    sql = """
    UPDATE customers 
    SET password = %s
    WHERE customers.user_id = %s
    """
    cur.execute(sql, (new_password, user_id))
    conn.commit()
    cur.close()
    
def update_password_employees(user_id, new_password):
    cur = conn.cursor()
    sql = """
    UPDATE employees 
    SET password = %s
    WHERE employees.user_id = %s
    """
    cur.execute(sql, (new_password, user_id))
    conn.commit()
    cur.close()
    
def update_name_customer(user_id, new_name):
    cur = conn.cursor()
    sql = """
    UPDATE customers 
    SET name = %s
    WHERE customers.user_id = %s
    """
        
    cur.execute(sql, (new_name, user_id))
    conn.commit()
    cur.close()
    
def update_name_employees(user_id, new_name):
    cur = conn.cursor()
    sql = """
    UPDATE employees 
    SET name = %s
    WHERE employees.user_id = %s
    """
            
    cur.execute(sql, (new_name, user_id))
    conn.commit()
    cur.close()

def select_balance(user_id):
    cur = conn.cursor()
    sql = """
        SELECT balance From accounts WHERE user_id = %s
    """
        
    cur.execute(sql, (user_id,))
    balance = cur.fetchone()
    cur.close()
    return balance[0]

def update_balance(user_id, amount):
    cur = conn.cursor()
    sql = """
    UPDATE accounts
    SET balance = %s
    WHERE accounts.user_id = %s
    """
    cur.execute(sql, (amount, user_id))
    conn.commit()
    cur.close()

def insert_balance(user_id):
    cur = conn.cursor()
    sql = """
    INSERT INTO Accounts(user_id, balance)
    VALUES (%s, 0)
    """
    cur.execute(sql, (user_id, ))
    conn.commit()
    cur.close()

def add_to_inventory(classid, instanceid, userid):
    cur = conn.cursor()
    sql = """
    INSERT INTO Inventory(classid, instanceid, user_id)
    VALUES (%s, %s, %s)
    """
    cur.execute(sql, (classid, instanceid, userid))
    conn.commit()
    cur.close()