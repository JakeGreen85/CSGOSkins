
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
	User_id integer REFERENCES Customers(User_id),
	Balance integer
);

CREATE TABLE IF NOT EXISTS Inventory(
	classid bigint,
	instanceid bigint,
	User_id integer REFERENCES Customers(User_id)
);