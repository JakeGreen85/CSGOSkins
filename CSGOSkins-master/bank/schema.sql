DROP TABLE IF EXISTS Accounts;
DROP TABLE IF EXISTS Assets;
DROP TABLE IF EXISTS Inventory;
DROP TABLE IF EXISTS Employees;
DROP TABLE IF EXISTS Customers;

CREATE TABLE IF NOT EXISTS Customers(
	User_id integer PRIMARY KEY,
	password varchar(120),
	name varchar(60)
);

CREATE TABLE IF NOT EXISTS Assets(
	classid bigint,
	instanceid bigint,
	name varchar(100),
	price int,
	icon_url varchar(300),
	quality varchar(100),
	PRIMARY KEY (classid, instanceid)
);

CREATE TABLE IF NOT EXISTS Employees(
	User_id integer PRIMARY KEY,
    name varchar(20),
    password varchar(120)
);

CREATE TABLE IF NOT EXISTS Accounts(
	User_id integer,
	Balance integer
);

CREATE TABLE IF NOT EXISTS Inventory(
	classid bigint,
	instanceid bigint,
	User_id integer
);

-- INSERT CUSTOMERS
INSERT INTO public.Customers(User_id, password, name)
VALUES (0001,'$2b$12$KFkp1IEMGT4QrWwjPGhE3ejOv6Z3pYhx/S4qOoFbanR2sMiZqgeJO', 'Jakob'), (0002, '$2b$12$KFkp1IEMGT4QrWwjPGhE3ejOv6Z3pYhx/S4qOoFbanR2sMiZqgeJO', 'Laust');

-- INSERT EMPLOYEES
INSERT INTO public.Employees(User_id, name, password)
VALUES (1001, 'Jakob', '$2b$12$KFkp1IEMGT4QrWwjPGhE3ejOv6Z3pYhx/S4qOoFbanR2sMiZqgeJO')
, (1002, 'Laust', '$2b$12$KFkp1IEMGT4QrWwjPGhE3ejOv6Z3pYhx/S4qOoFbanR2sMiZqgeJO');

-- INSERT ACCOUNTS
INSERT INTO public.accounts(User_id, Balance) VALUES (0001, 5000), (0002, 10000), (1001, 50000), (1002, 25000);