import sqlite3
import datetime

PATH = 'DBFiles/coffeeShop.db'

class Database:
    def __init__(self):
        self.conn = sqlite3.connect(PATH, isolation_level=None)
    
    def execute(self, sql, parameters=[]):
        c = self.conn.cursor()
        c.execute(sql, parameters)
        return self.conn.commit()

    def select(self, sql, parameters=[]):
        c = self.conn.cursor()
        c.execute(sql, parameters)
        return c.fetchall()

    def getPermissions(self, accessID):
        if(accessID >= 0):
            data = self.select( 'SELECT Type FROM User WHERE ID=?', [accessID])
            
            if( len(data) == 0):
                return -1 #something went wrong
            
            if(data[0][0] == 'CUSTOMER'):
                return 0 #basic level access
            elif(data[0][0] == 'BARISTA'):
                return 1 #Access to all orders, adding items, editing items
            elif(data[0][0] == 'MANAGER'):
                return 2 #Access to nearly everything. (Fixing and editing orders directly, Changing user type, etc.)
            
        return -1 #invalid access level
        
    
    def apiGetItems(self, n, offset):
        # obtained from the slides.
        # note that only name, image, and available are neccessary now but the other may be used in later assignments.
        # order by length of the number then by text. This way, b10 will not appear second when b2 should appear instead.

        data = self.select( 'SELECT * FROM Item ORDER BY Name ASC LIMIT ? OFFSET ?', [n, offset])
        return [{
            'id': d[0],
            'type': d[1],
            'price': d[2],
            'name': d[3],
            'image': d[4],
            'description': d[5]
        } for d in data]

    def apiAddItem(self, accessID, itemType, itemName, itemPrice, itemImage, itemDescription):
        if(self.getPermissions(accessID) >= 1 and accessID != -1):
            data = self.execute( 'INSERT INTO ITEM (Type, Name, Price, Image, Description) VALUES (?, ?, ?, ?, ?)', [itemType, itemName, itemPrice, itemImage, itemDescription])
            
            #Should check if it actually updated to give valid or useful information
            return {
                'Status': 'Successful'
            }
        else:
            return {
                'Status': 'Failed',
                'Reason': 'Invalid Permissions'
            }

    def apiDeleteItem(self, accessID, itemID):
        if(self.getPermissions(accessID) >= 1 and accessID != -1):
            data = self.execute( 'DELETE FROM Item WHERE id=?', [itemID])
            #Should check if it actually updated to give valid or useful information
            return {
                'Status': 'Successful'
            }
        else:
            return {
                'Status': 'Failed',
                'Reason': 'Invalid Permissions'
            }
    
    #get items in the cart for user
    def apiGetCart(self, userID):
        if(userID != -1):
            command = 'SELECT CartItem.Count, Item.Name, Item.Price, Item.Image '\
                                'FROM CartItem '\
                                'INNER JOIN Item ON Item.ID=CartItem.ItemID '\
                                'WHERE CartItem.UserID=?'
            
            data = self.select( command, [userID])
            
            return [{
                'cartItemCount': d[0],
                'itemName': d[1],
                'itemPrice': d[2],
                'itemImage': d[3]
            } for d in data]
        else:
            return {
                'Status': 'Failed',
                'Reason': 'Invalid Permissions'
            }
    
    #get all orders from user
    def apiGetOrders(self, accessID, userID):
        if(self.getPermissions(accessID) >= 1 or accessID==userID and accessID != -1 and userID != -1):
            data = self.select('SELECT OrderInfo.ID, OrderInfo.Date, OrderItem.Count, Item.Name, Item.Price, Item.Image '\
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
            return {
                'Status': 'Failed',
                'Reason': 'Invalid Permissions'
            }
    
    def apiGetAllOrders(self, accessID):
        if(self.getPermissions(accessID) >= 1 and accessID != -1):
            data = self.select('SELECT OrderInfo.ID, OrderInfo.Date, OrderItem.Count, Item.Name, Item.Price, Item.Image '\
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
            return {
                'Status': 'Failed',
                'Reason': 'Invalid Permissions'
            }
    
    def apiAddToCart(self, accessID, userID, itemID, count):
        if(userID != -1):
            # Should check if it already exist. If so, update instead of insert
            data = self.execute('INSERT INTO CartItem (UserID, ItemID, Count) VALUES (?, ?, ?)', [userID, itemID, count])
            
            #Should check if it actually updated to give valid or useful information
            return {
                'Status': 'Successful'
            }
        else:
            return {
                'Status': 'Failed',
                'Reason': 'Invalid Permissions'
            }
    
    #Research Transactions in sqlite. They should be used here to add pending orders
    def apiCreateOrder(self, userID):
        if(userID != -1):

            dateFormat = '%Y-%m-%d %I:%M %p'
            dateString = datetime.now().strftime(dateFormat)
            data = self.execute("INSERT INTO OrderInfo (UserID, Date, Status) VALUES (?, ?, 'Pending')", [userID, dateString])

            # add all items in the cart to the order and remove them from the cart
            # sqlite has the function last_insert_rowid(). Should be specific to this connection/session. If not, a select will do just fine. Don't know how to use it in python though.
            data = self.select('SELECT ID From OrderInfo WHERE UserID=? ORDER BY ID DESC', [userID])

            #add all from cart
            self.execute('INSERT INTO OrderItem (OrderID, ItemID, Count) '\
                         'SELECT ?, ci.ItemID, ci.Count FROM CartItem as ci WHERE ci.UserID=?', [data[0][0], userID])
            
            #remove from the cart
            self.execute('DELETE FROM CartItem WHERE UserID=?', [userID])

            #!Should send email confirmation here if we have time.

            #Should check if it actually updated to give valid or useful information
            return {
                'Status': 'Successful'
            }
        else:
            #Tried to add an order for a user. Dangerous if allowed because of fraud.
            return {
                'Status': 'Failed',
                'Reason': 'Invalid Permissions'
            }
    
    def apiGetPendingOrders(self, accessID):
        if(self.getPermissions(accessID) >= 1):
            data = self.select("SELECT * FROM OrderInfo WHERE Status='Pending'")

            #Not including status message since that is mostly for the customer so they know why their order was canceled.
            return [{
                'OrderID': d[0],
                'UserID': d[1],
                'Status': d[2],
                'Date': d[3]
            } for d in data]
        else:
            return {
                'Status': 'Failed',
                'Reason': 'Invalid Permissions'
            }

    def apiApproveOrder(self, accessID, orderID):
        if(self.getPermissions(accessID) >= 1 and orderID != -1):
            self.execute("UPDATE OrderInfo SET Status='Approved' WHERE ID=?", [orderID])

            #!Should send email confirmation here if we have time.

            #Should check if it actually updated to give valid or useful information
            return {
                'Status': 'Successful'
            }
        else:
            return {
                'Status': 'Failed',
                'Reason': 'Invalid Permissions or Order ID'
            }
    
    def apiCancelOrder(self, accessID, userID, orderID, message):
        if((self.getPermissions(accessID) >= 1 or accessID==userID) and orderID != -1 and accessID != -1):

            #Message provided by barista/manager or if user, then the message 'User Submitted' or something
            #May be better to just delete the order entirely. It does not hurt to keep it along with the reason though so the default will be to keep them.
            
            if(self.getPermissions(accessID) >= 1):
                #can update any order
                self.execute("UPDATE OrderInfo SET Status='Canceled', StatusMessage=? WHERE ID=?", [message, orderID])
            else:
                #Can only update orders that belong to the user.
                self.execute("UPDATE OrderInfo SET Status='Canceled', StatusMessage=? WHERE ID=? AND UserID=?", [message, orderID, userID])

            #!Should send email confirmation here if we have time.

            #Should check if it actually updated to give valid or useful information
            return {
                'Status': 'Successful'
            }
        else:
            return {
                'Status': 'Failed',
                'Reason': 'Invalid Permissions or Order ID'
            }
        
            return "Permission Denied" #Tried to add an order for a user. Dangerous if allowed because of fraud.

    def apiSetUserToEmployee(self, accessID, userID):
        if(self.getPermissions(accessID) >= 2):
            self.execute("UPDATE User SET Type=? WHERE ID=?", ['BARISTA', userID])
            #Should check if it actually updated to give valid or useful information
            return {
                'Status': 'Successful'
            }
        else:
            return {
                'Status': 'Failed',
                'Reason': 'Invalid Permissions'
            }
        
    def get_user(self, username):
        data = self.select(
            'SELECT * FROM user WHERE username=?', [username])
        if data:
            d = data[0]
            return {
                'id': d[0],
                'userType': d[1],
                'email': d[2],
                'username': d[3],
                'EncryptPass': d[4]
            }
        else:
            return None
    
    def create_user(self, email, username, EncryptPass, userType):
        self.execute('INSERT INTO user (Type, Email, Username, EncryptPass) VALUES (?, ?, ?, ?)',
                     [userType, email, username, EncryptPass])
    
    def close(self):
        self.conn.close()