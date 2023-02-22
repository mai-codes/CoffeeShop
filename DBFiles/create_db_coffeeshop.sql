
CREATE TABLE USER (
	ID INTEGER PRIMARY KEY,
	TYPE TEXT NOT NULL, -- Should be Customer, Barista, Manager, etc.
	Username TEXT NOT NULL,
	EncryptPass TEXT NOT NULL
);

CREATE TABLE ORDERINFO (
	ID INTEGER PRIMARY KEY,
	UserID INTEGER NOT NULL
);

CREATE TABLE ITEM (
	ID INTEGER PRIMARY KEY,
	Image TEXT,
	Description TEXT
);

CREATE TABLE ORDERITEM (
	ID INTEGER PRIMARY KEY,
	OrderID INTEGER NOT NULL,
	ItemID INTEGER NOT NULL,
	Count INTEGER
);

--Probably should have a cart table to store what was in the cart
