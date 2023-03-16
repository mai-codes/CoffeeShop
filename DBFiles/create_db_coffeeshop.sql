
-- All orders should be visible by an admin of some sorts.
-- Use Transactions (sql thing) to allow pending orders.
CREATE TABLE IF NOT EXISTS OrderInfo (
	ID INTEGER PRIMARY KEY,
	UserID TEXT NOT NULL,
	Status TEXT NOT NULL,		--Status (Accepted, Processing, Canceled, etc.)
	Date DATETIME,
	StatusMessage Text		--Status Message Reason for failure
);

-- Some item that can be ordered.
-- Note that here, all prices for each size are listed. When submitting the item to the cart, it will have the size but not the price of the size.
-- This is due to possible price changes for a given size.
CREATE TABLE IF NOT EXISTS Item (
	ID INTEGER PRIMARY KEY,
	Type INTEGER NOT NULL, -- Should be coffee or tea so that it is possible to browse just one type of drink.
	SMPrice SMALLMONEY NOT NULL,
	MDPrice SMALLMONEY NOT NULL,
	LGPrice SMALLMONEY NOT NULL,
	Name TEXT,
	Image TEXT,
	Description TEXT
);

-- Done to have clean list not stored in a csv style. Items are tied to the appropriate order
-- OrderItem will have a separate price since order history should contain what you originally paid for the item.
CREATE TABLE IF NOT EXISTS OrderItem (
	ID INTEGER PRIMARY KEY,
	OrderID INTEGER NOT NULL,
	ItemID INTEGER NOT NULL,
	Size TEXT NOT NULL,
	Price SMALLMONEY NOT NULL,
	Count INTEGER
);

-- Items tied to a users cart. This should be done through cookies as well but
-- This is needed so carts are synced through devices and browsers.
-- Note that the price of an item can change based on size and date. (Price in order history should be what you paid and not the current price)
CREATE TABLE IF NOT EXISTS CartItem (
	ID INTEGER PRIMARY KEY,
	UserID TEXT NOT NULL,
	ItemID INTEGER NOT NULL,
	Size TEXT NOT NULL,
	Count INTEGER
);