import sqlite3
from datetime import datetime

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
    
    
    def apiGetItems(self, n, offset):
        # obtained from the slides.
        # note that only name, image, and available are neccessary now but the other may be used in later assignments.
        # order by length of the number then by text. This way, b10 will not appear second when b2 should appear instead.

        data = self.select( 'SELECT * FROM Item ORDER BY Name ASC LIMIT ? OFFSET ?', [n, offset])
        return [{
            'id': d[0],
            'type': d[1],
            'smallprice': d[2],
            'mediumprice': d[3],
            'largeprice': d[4],
            'name': d[5],
            'image': d[6],
            'description': d[7]
        } for d in data]

    def apiAddItem(self, itemType, itemName, smallPrice, mediumPrice, largePrice, itemImage, itemDescription):
        try:
            self.execute( 'INSERT INTO ITEM (Type, Name, SMPrice, MDPrice, LGPrice, Image, Description) VALUES (?, ?, ?, ?, ?, ?, ?)', [itemType, itemName, smallPrice, mediumPrice, largePrice, itemImage, itemDescription])
            
            #Should check if it actually updated to give valid or useful information
            return {
                'Status': 'Successful'
            }
        except:
            return {
                'Status': 'Failed',
                'Reason': 'Invalid Permissions'
            }

    def apiDeleteItem(self, itemID):
        try:
            self.execute( 'DELETE FROM Item WHERE id=?', [itemID])
            #Should check if it actually updated to give valid or useful information
            return {
                'Status': 'Successful'
            }
        except:
            return {
                'Status': 'Failed',
                'Reason': 'Invalid Permissions'
            }
    
    #get items in the cart for user
    def apiGetCart(self, userID):
        if(userID != None):
            #updated to get item size and price based on its size
            command = "SELECT CartItem.ID, CartItem.Count, Item.Name, CartItem.Size, IIF(CartItem.Size='Large', Item.LGPrice, IIF(CartItem.Size='Medium', Item.MDPrice, Item.SMPrice) ), Item.Image "\
                                'FROM CartItem '\
                                'INNER JOIN Item ON Item.ID=CartItem.ItemID '\
                                'WHERE CartItem.UserID=?'
            
            data = self.select( command, [userID])
            
            return [{
                'id': d[0],
                'itemCount': d[1],
                'itemName': d[2],
                'itemSize': d[3],
                'itemPrice': d[4],
                'itemImage': d[5]
            } for d in data]
        else:
            return {
                'Status': 'Failed',
                'Reason': 'Invalid Permissions'
            }
    
    #get all orders from user
    def apiGetOrders(self, userID):
        if(userID != None):
            #Adjusted to get order item price which may not be the same as the current items price and its size.
            data = self.select('SELECT OrderInfo.ID, OrderInfo.Date, OrderItem.Count, Item.Name, OrderItem.Size, OrderItem.Price, Item.Image, OrderInfo.Status, OrderInfo.StatusMessage '\
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
                'itemSize': d[4],
                'itemPrice': d[5],
                'itemImage': d[6],
                'orderStatus': d[7],
                'statusMessage': d[8]
            } for d in data]
        else:
            return {
                'Status': 'Failed',
                'Reason': 'Invalid Permissions'
            }
    
    def apiGetAllOrders(self):
        data = self.select('SELECT OrderInfo.ID, OrderInfo.Date, OrderItem.Count, Item.Name, OrderItem.Size, OrderItem.Price, Item.Image, OrderInfo.Status, OrderInfo.StatusMessage '\
                            'FROM OrderInfo '\
                            'INNER JOIN OrderItem ON OrderInfo.ID=OrderItem.OrderID '\
                            'INNER JOIN Item ON Item.ID=OrderItem.ItemID ORDER BY OrderInfo.Date DESC')

        return [{
            'orderID': d[0],
            'orderDate': d[1],
            'itemCount': d[2],
            'itemName': d[3],
            'itemSize': d[4],
            'itemPrice': d[5],
            'itemImage': d[6],
            'orderStatus': d[7],
            'statusMessage': d[8]
        } for d in data]
    
    def apiAddToCart(self, userID, itemID, size, count):
        if(userID != None):
            # Should check if it already exist. If so, update instead of insert
            self.execute('INSERT INTO CartItem (UserID, ItemID, Size, Count) VALUES (?, ?, ?, ?)', [userID, itemID, size, count])
            
            #Should check if it actually updated to give valid or useful information
            return {
                'Status': 'Successful'
            }
        else:
            return {
                'Status': 'Failed',
                'Reason': 'Invalid Permissions'
            }
    
    def apiRemoveFromCart(self, userID, cartItemID):
        if(userID != None):
            # Should check if it already exist. If so, update instead of insert
            self.execute('DELETE FROM CartItem WHERE UserID=? AND ID=?', [userID, cartItemID])
            
            #Should check if it actually updated to give valid or useful information
            return {
                'Status': 'Successful'
            }
        else:
            return {
                'Status': 'Failed',
                'Reason': 'Invalid Permissions'
            }
    
    def apiCreateOrder(self, userID):
        if(userID != None):

            # Only add if there are items in the cart
            data = self.select('SELECT * FROM CartItem Where CartItem.UserID=?', [userID])
            if(len(data) == 0):
                return {
                    'Status': 'Failed',
                    'Reason': 'No Items in cart'
                }
            
            dateFormat = '%Y-%m-%d %I:%M %p'
            dateString = datetime.now().strftime(dateFormat)
            data = self.execute("INSERT INTO OrderInfo (UserID, Date, Status) VALUES (?, ?, 'Pending')", [userID, dateString])

            # add all items in the cart to the order and remove them from the cart
            # sqlite has the function last_insert_rowid(). Should be specific to this connection/session. If not, a select will do just fine. Don't know how to use it in python though.
            data = self.select('SELECT ID From OrderInfo WHERE UserID=? ORDER BY ID DESC', [userID])

            #add all from cart
            self.execute('INSERT INTO OrderItem (OrderID, ItemID, Size, Price, Count) '\
                         "SELECT ?, ci.ItemID, ci.Size, IIF(ci.Size='Large', Item.LGPrice, IIF(ci.Size='Medium', Item.MDPrice, Item.SMPrice) ), ci.Count FROM CartItem as ci "\
                         "INNER JOIN Item ON ci.ItemID=Item.ID "\
                         "WHERE ci.UserID=?", [data[0][0], userID])

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
    
    def apiGetPendingOrders(self):
        data = self.select('SELECT OrderInfo.ID, OrderInfo.Date, OrderItem.Count, Item.Name, OrderItem.Size, OrderItem.Price, Item.Image, OrderInfo.Status'\
                            'FROM OrderInfo '\
                            'INNER JOIN OrderItem ON OrderInfo.ID=OrderItem.OrderID '\
                            'INNER JOIN Item ON Item.ID=OrderItem.ItemID '\
                            "WHERE Status='Pending' "\
                            'ORDER BY OrderInfo.Date ASC')

        #Not including status message since that is mostly for the customer so they know why their order was canceled.
        return [{
            'orderID': d[0],
            'orderDate': d[1],
            'itemCount': d[2],
            'itemName': d[3],
            'itemSize': d[4],
            'itemPrice': d[5],
            'itemImage': d[6],
            'orderStatus': d[7]
        } for d in data]

    def apiApproveOrder(self, orderID):
        self.execute("UPDATE OrderInfo SET Status='Approved' WHERE ID=?", [orderID])

        #!Should send email confirmation here if we have time.

        #Should check if it actually updated to give valid or useful information
        return {
            'Status': 'Successful'
        }
    
    def apiCancelOrderEmployee(self, orderID, message):
        #can update any order
        self.execute("UPDATE OrderInfo SET Status='Canceled', StatusMessage=? WHERE ID=?", [message, orderID])
        
        #!Should send email confirmation here if we have time.

        return {
            'Status': 'Successful'
        }
    
    def apiCancelOrder(self, userID, orderID, message):
        self.execute("UPDATE OrderInfo SET Status='Canceled', StatusMessage=? WHERE ID=? AND UserID=?", [message, orderID, userID])

        #!Should send email confirmation here if we have time.

        #Should check if it actually updated to give valid or useful information
        return {
            'Status': 'Successful'
        }
    
    def close(self):
        self.conn.close()