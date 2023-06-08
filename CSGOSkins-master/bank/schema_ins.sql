DELETE FROM Accounts;
DELETE FROM Employees;
DELETE FROM Customers;
DELETE FROM Assets;
DELETE FROM Inventory;

-- INSERT CUSTOMERS
INSERT INTO public.Customers(User_id, password, name)
VALUES (0001,'$2b$12$KFkp1IEMGT4QrWwjPGhE3ejOv6Z3pYhx/S4qOoFbanR2sMiZqgeJO', 'Jakob'), (0002, '$2b$12$KFkp1IEMGT4QrWwjPGhE3ejOv6Z3pYhx/S4qOoFbanR2sMiZqgeJO', 'Laust');


-- INSERT EMPLOYEES
INSERT INTO public.Employees(User_id, name, password)
VALUES (1001, 'Jakob', '$2b$12$KFkp1IEMGT4QrWwjPGhE3ejOv6Z3pYhx/S4qOoFbanR2sMiZqgeJO')
, (1002, 'Laust', '$2b$12$KFkp1IEMGT4QrWwjPGhE3ejOv6Z3pYhx/S4qOoFbanR2sMiZqgeJO');

-- INSERT ACCOUNTS
INSERT INTO public.accounts(User_id, Balance) VALUES (0001, 5000), (0002, 10000), (1001, 50000), (1002, 25000);

-- INSERT ASSETS
INSERT INTO public.Assets(classid, instanceid, name, price, quality, icon_url) VALUES (310776843, 188530139, 'MP9 | Rose Iron', 682, 'Exterior: Minimal Wear', '-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXH5ApeO4YmlhxYQknCRvCo04DEVlxkKgpou6r8FAZt7OfAfi9M9eOkm5OOqPrkaoTdn2xZ_Itw27GW892m3ATgrhE9am-ncYCXcFA6MlHUr1m7wenn08S9tMnBnXUwpGB8sjkI-Dv2'), (5361356205, 188530139,'Souvenir SSG 08 | Tropical Storm',384,'Exterior: Well-Worn','-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXH5ApeO4YmlhxYQknCRvCo04DEVlxkKgpopamie19fwOP3YTxO4eOlnIGPmODLPr7Vn35cpsZ137-Zrdvz3QXg_EQ-MTqiINXBdVdvZFHYqAC9k7rqgpXousnBwXR9-n51Y41l40A');

-- INSERT INVENTORY
INSERT INTO public.Inventory(classid, instanceid, User_id) VALUES (310776843,188530139, 0001), (5361356205, 188530139, 0002);