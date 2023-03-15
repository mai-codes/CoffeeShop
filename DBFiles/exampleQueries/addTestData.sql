-- 4 users
-- INSERT INTO User (Type, Email, Username, EncryptPass) VALUES ('CUSTOMER', 'abc@123.com', 'person1', 'password1');
-- INSERT INTO User (Type, Email, Username, EncryptPass) VALUES ('CUSTOMER', '123@abc.com', 'person2', 'password2');
-- INSERT INTO User (Type, Email, Username, EncryptPass) VALUES ('BARISTA', 'bar@123.com', 'Employee', 'password3');
-- INSERT INTO User (Type, Email, Username, EncryptPass) VALUES ('MANAGER', 'man@123.com', 'Manager', 'password4');

-- 3 Orders
INSERT INTO OrderInfo(UserID, Status, Date) VALUES (1, 'Completed', '2022-01-15 10:34:09 AM');
INSERT INTO OrderInfo(UserID, Status, Date) VALUES (2, 'Completed', '2022-01-20 09:30:00 AM');
INSERT INTO OrderInfo(UserID, Status, Date) VALUES (1, 'Completed', '2022-02-15 11:20:15 AM');

-- 5 Items
INSERT INTO Item(Type, Name, SMPrice, MDPrice, LGPrice, Image, Description) VALUES (0, 'Mocha', 1.25, 2.00, 3.00, 'mocha.png', 'Alt text for Mocha');
INSERT INTO Item(Type, Name, SMPrice, MDPrice, LGPrice, Image, Description) VALUES (1, 'Match Latte', 3.00, 4.00, 5.00, 'matcha.png', 'Alt text for Match Latte');
INSERT INTO Item(Type, Name, SMPrice, MDPrice, LGPrice, Image, Description) VALUES (1, 'Iced Lemon Tea', 3.00, 4.00, 5.00, 'lemon.png', 'Alt text for lemon tea');
INSERT INTO Item(Type, Name, SMPrice, MDPrice, LGPrice, Image, Description) VALUES (0, 'Americano', 2.25, 3.25, 4.25, 'americano.jpg', 'Alt text for americano');
INSERT INTO Item(Type, Name, SMPrice, MDPrice, LGPrice, Image, Description) VALUES (1, 'Earl Grey Tea', 3.00, 4.00, 5.00, 'earlGrey.jpg', 'Alt text for earl grey tea');
INSERT INTO Item(Type, Name, SMPrice, MDPrice, LGPrice, Image, Description) VALUES (0, 'Espresso', 2.25, 3.25, 4.25, 'espresso.png', 'Alt text for espresso');


-- 6 Order Items (1st order has one unique thing, 2nd has 3 unique things, 3rd has 2 unique things)
INSERT INTO OrderItem(OrderID, ItemID, Size, Price, Count) VALUES (1, 1, 'Small', 2.00, 2);
INSERT INTO OrderItem(OrderID, ItemID, Size, Price, Count) VALUES (2, 2, 'Small', 1.50, 1);
INSERT INTO OrderItem(OrderID, ItemID, Size, Price, Count) VALUES (2, 4, 'Medium', 3.00, 1);
INSERT INTO OrderItem(OrderID, ItemID, Size, Price, Count) VALUES (2, 1, 'Medium', 2.00, 1);
INSERT INTO OrderItem(OrderID, ItemID, Size, Price, Count) VALUES (3, 5, 'Small', 1.70, 1);
INSERT INTO OrderItem(OrderID, ItemID, Size, Price, Count) VALUES (3, 1, 'Large', 4.50, 2);

-- Only the first user has things in their cart
INSERT INTO CartItem(UserID, ItemID, Size, Count) VALUES (1, 3, 'Small', 1);
INSERT INTO CartItem(UserID, ItemID, Size, Count) VALUES (1, 2, 'Medium', 1);
