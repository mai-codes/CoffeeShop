import sqlite3


class Database:
    def __init__(self, path):
        self.conn = sqlite3.connect(path)
    
    def select(self, sql, parameters=[]):
        c = self.conn.cursor()
        c.execute(sql, parameters)
        return c.fetchall()

    def execute(self, sql, parameters=[]):
        c = self.conn.cursor()
        c.execute(sql, parameters)
        self.conn.commit()
    
    def getPermissions(self, accessID):
        if(accessID >= 0):
            data = self.execute( 'SELECT Type FROM User WHERE ID=?', [accessID])
            
            if( len(data) == 0):
                return -1 #something went wrong
            
            if(data[0][0] == 'CUSTOMER'):
                return 0 #basic level access
            elif(data[0][0] == 'BARISTA'):
                return 1 #Access to all orders, adding items, editing items
            elif(data[0][0] == 'MANAGER'):
                return 2 #Access to nearly everything. (Fixing and editing orders directly, Changing user type, etc.)
            
        return -1 #invalid access level
        
    
    def get_items(self, n, offset):
        # obtained from the slides.
        # note that only name, image, and available are neccessary now but the other may be used in later assignments.
        # order by length of the number then by text. This way, b10 will not appear second when b2 should appear instead.

        data = self.select( 'SELECT * FROM Item ORDER BY Item.id ASC ') #LIMIT ? OFFSET ?', [n, offset]
        return [{
            'id': d[0],
            'type': d[1],
            'price': d[2],
            'name': d[3],
            'image': d[4],
            'description': d[5]
        } for d in data]
    
    def get_num_items(self):
        data = self.select('SELECT COUNT(*) FROM Item')
        return data[0][0]
    
    def apiAddItem(self, accessID, itemType, itemName, itemPrice, itemImage, itemDescription):
        if(self.getPermissions(accessID) >= 1 and accessID != -1):
            data = self.execute( 'INSERT INTO ITEM (Type, Name, Price, Image, Description) VALUES (?, ?, ?, ?, ?)', [itemType, itemName, itemPrice, itemImage, itemDescription])
            return "" #should return if successful or not
        else:
            return "Permission Denied"

    def apiDeleteItem(self, accessID, itemID):
        if(self.getPermissions(accessID) >= 1 and accessID != -1):
            data = self.execute( 'DELETE FROM Item WHERE id=?', [itemID])
            return "" #should return if successful or not
        else:
            return "Permission Denied"
    
    #get items in the cart for user
    def apiGetCart(self, accessID, userID):
        if(self.getPermissions(accessID) >= 2 or accessID==userID and accessID != -1 and userID != -1):
            command = 'SELECT CartItem.Count, Item.Name, Item.Price, Item.Image '\
                                'FROM CartItem '\
                                'INNER JOIN Item ON Item.ID=CartItem.ItemID '\
                                'WHERE CartItem.UserID=?'
            print(command)
            data = self.execute( command, [userID])
            
            return [{
                'cartItemCount': d[0],
                'itemName': d[1],
                'itemPrice': d[2],
                'itemImage': d[3]
            } for d in data]
        else:
            return "Permission Denied" #Tried to access the cart of another user and is not the manager
    
    #get all orders from user
    def apiGetOrders(self, accessID, userID):
        if(self.getPermissions(accessID) >= 1 or accessID==userID and accessID != -1 and userID != -1):
            data = self.execute('SELECT OrderInfo.ID, OrderInfo.Date, OrderItem.Count, Item.Name, Item.Price, Item.Image '\
                                'FROM OrderInfo '\
                                'INNER JOIN OrderItem ON OrderInfo.ID=OrderItem.OrderID '\
                                'INNER JOIN Item ON Item.ID=OrderItem.ItemID '\
                                'WHERE OrderInfo.UserID=? '\
                                'ORDER BY OrderInfo.Date DESC', [userID])

            return [{
                'orderID': d[0],
                'orderDate': d[1],
                'itemCount': d[2],
                'itemName': d[3],
                'itemPrice': d[4],
                'itemImage': d[5]
            } for d in data]
        else:
            return "Permission Denied" #Tried to access the orders of users and is not an employee
    
    def apiGetAllOrders(self, accessID):
        if(self.getPermissions(accessID) >= 1 and accessID != -1):
            data = self.execute('SELECT OrderInfo.ID, OrderInfo.Date, OrderItem.Count, Item.Name, Item.Price, Item.Image '\
                                'FROM OrderInfo '\
                                'INNER JOIN OrderItem ON OrderInfo.ID=OrderItem.OrderID '\
                                'INNER JOIN Item ON Item.ID=OrderItem.ItemID ORDER BY OrderInfo.Date DESC')

            return [{
                'orderID': d[0],
                'orderDate': d[1],
                'itemCount': d[2],
                'itemName': d[3],
                'itemPrice': d[4],
                'itemImage': d[5]
            } for d in data]
        else:
            return "Permission Denied" #Tried to access the orders of users and is not an employee
    
    def apiAddToCart(self, accessID, userID, itemID, count):
        if(self.getPermissions(accessID) >= 2 or accessID==userID and accessID != -1 and userID != -1):
            # Should check if it already exist. If so, update instead of insert
            data = self.execute('INSERT INTO CartItem (UserID, ItemID, Count) VALUES (?, ?, ?)', [userID, itemID, count])
            return "" #Should return if successful
        else:
            return "Permission Denied" #Tried to access the orders of users and is not an employee
    
    #Research Transactions in sqlite. They should be used here to add pending orders
    def apiAddOrder(self, accessID, userID):
        if(accessID == userID and accessID != -1):
            dateFormat = '%Y-%m-%d %I:%M %p'
            dateString = datetime.now().strftime(dateFormat)
            data = self.execute('INSERT INTO OrderInfo (UserID, Date) VALUES (?, ?)', [userID, dateString])

            # add all items in the cart to the order and remove them from the cart
            # sqlite has the function last_insert_rowid(). Should be specific to this connection/session. If not, a select will do just fine. Don't know how to use it in python though.
            data = self.execute('SELECT ID From OrderInfo WHERE UserID=? ORDER BY ID DESC', [userID])

            #add all from cart
            self.execute('INSERT INTO OrderItem (OrderID, ItemID, Count) '\
                         'SELECT ?, ci.ItemID, ci.Count FROM CartItem as ci WHERE ci.UserID=?', [data[0][0], userID])

            #remove from the cart
            self.execute('DELETE FROM CartItem WHERE UserID=?', [userID])

            return ""
        else:
            return "Permission Denied" #Tried to add an order for a user. Dangerous if allowed because of fraud.
    def close(self):
        self.conn.close()