
-- This is assuming that we store the password and username here. We require the Email though for order confirmation.
CREATE TABLE User (
	ID INTEGER PRIMARY KEY,
	Type TEXT NOT NULL, -- Should be Customer, Barista, Manager, etc.
	Email TEXT NOT NULL, -- Can be used for resetting password and sending order confirmations
	Username TEXT NOT NULL,
	EncryptPass TEXT NOT NULL
);

-- All orders should be visible by an admin of some sorts.
CREATE TABLE OrderInfo (
	ID INTEGER PRIMARY KEY,
	UserID INTEGER NOT NULL,
	Date DATETIME
);

-- Some item that can be ordered.
-- Forgot about size. That can be fixed by adding them as different items all together.
-- This makes the cart easier too and allows for different images for each item. Also, I'm a little lazy.
CREATE TABLE Item (
	ID INTEGER PRIMARY KEY,
	Type INTEGER NOT NULL, -- Should be coffee or tea so that it is possible to browse just one type of drink.
	Name TEXT,
	Image TEXT,
	Description TEXT
);

-- Done to have clean list not stored in a csv style. Items are tied to the appropriate order
CREATE TABLE OrderItem (
	ID INTEGER PRIMARY KEY,
	OrderID INTEGER NOT NULL,
	ItemID INTEGER NOT NULL,
	Count INTEGER
);

-- Items tied to a users cart. This should be done through cookies as well but
-- This is needed so carts are synced through devices and browsers.
CREATE TABLE CartItem (
	ID INTEGER PRIMARY KEY,
	UserID INTEGER NOT NULL,
	ItemID INTEGER NOT NULL,
	Count INTEGER
);