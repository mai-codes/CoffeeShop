-- 4 users
INSERT INTO User (Type, Email, Username, EncryptPass) VALUES ('CUSTOMER', 'abc@123.com', 'person1', 'password1');
INSERT INTO User (Type, Email, Username, EncryptPass) VALUES ('CUSTOMER', '123@abc.com', 'person2', 'password2');
INSERT INTO User (Type, Email, Username, EncryptPass) VALUES ('BARISTA', 'bar@123.com', 'Employee', 'password3');
INSERT INTO User (Type, Email, Username, EncryptPass) VALUES ('MANAGER', 'man@123.com', 'Manager', 'password4');

-- 3 Orders
INSERT INTO OrderInfo(UserID, Date) VALUES (0, '2022-01-15 10:34:09 AM');
INSERT INTO OrderInfo(UserID, Date) VALUES (1, '2022-01-20 09:30:00 AM');
INSERT INTO OrderInfo(UserID, Date) VALUES (0, '2022-02-15 11:20:15 AM');

-- 5 Items
INSERT INTO Item(Type, Name, Image, Description) VALUES (0, 'House Blend', 'image1.jpg', 'Our local specialty');
INSERT INTO Item(Type, Name, Image, Description) VALUES (0, 'Americano', 'image2.jpg', 'More stuff about coffee');
INSERT INTO Item(Type, Name, Image, Description) VALUES (0, 'Espresso', 'image3.jpg', 'Provides a ton of energy for the day. (Results may vary)');
INSERT INTO Item(Type, Name, Image, Description) VALUES (1, 'Jasmine Green Tea', 'image4.jpg', 'Some stuff about tea');
INSERT INTO Item(Type, Name, Image, Description) VALUES (1, 'Earl Grey Tea', 'image5.jpg', 'Insert later');

-- 6 Order Items (1st order has one unique thing, 2nd has 3 unique things, 3rd has 2 unique things)
INSERT INTO OrderItem(OrderID, ItemID, Count) VALUES (0, 0, 2);
INSERT INTO OrderItem(OrderID, ItemID, Count) VALUES (1, 1, 1);
INSERT INTO OrderItem(OrderID, ItemID, Count) VALUES (1, 3, 1);
INSERT INTO OrderItem(OrderID, ItemID, Count) VALUES (1, 0, 1);
INSERT INTO OrderItem(OrderID, ItemID, Count) VALUES (2, 4, 1);
INSERT INTO OrderItem(OrderID, ItemID, Count) VALUES (2, 0, 2);

-- Only the first user has things in their cart
INSERT INTO CartItem(UserID, ItemID, Count) VALUES (0, 3, 1);
INSERT INTO CartItem(UserID, ItemID, Count) VALUES (0, 2, 1);
