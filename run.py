import os

from datetime import datetime
from flask import Flask, g, json, render_template, request

app = Flask(__name__)

import sqlite3

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('DBFiles/coffeeShop.db', isolation_level=None)
    
    def execute(self, sql, parameters=[]):
        c = self.conn.cursor()
        c.execute(sql, parameters)
        return c.fetchall()
    
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
        
    
    def apiGetItems(self, n, offset):
        # obtained from the slides.
        # note that only name, image, and available are neccessary now but the other may be used in later assignments.
        # order by length of the number then by text. This way, b10 will not appear second when b2 should appear instead.

        data = self.execute( 'SELECT * FROM Item ORDER BY Name ASC LIMIT ? OFFSET ?', [n, offset])
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

# Copied from the lecture slides.
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = Database()
    return db

# Copied from the lecture slides.
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/api/getItems', methods=['GET'])
def apiGetItems():
    n = int(request.args.get('n', default=20)) #Assuming that we don't have enough drinks to need more than one page
    offset = int(request.args.get('offset', default=0))
    items = get_db().apiGetItems(n, offset)
    return json.jsonify(items)

@app.route('/api/deleteItem', methods=['DELETE'])
def apiDeleteItem():
    accessID = int(request.args.get('accessID', default=-1)) #negative id. Probably should use a better way to get the current users id.
    id = int(request.args.get('id', default=-1)) #negative id should not exist
    get_db().apiDeleteItem(accessID, id)
    return json.jsonify("{'Success': 'true'}") #something like this but not always successful

@app.route('/api/getCart', methods=['GET'])
def apiGetCart():
    accessID = int(request.args.get('accessID', default=-1)) #negative id. Probably should use a better way to get the current users id.
    id = int(request.args.get('id', default=-1)) #negative id should not exist
    cartItems = get_db().apiGetCart(accessID, id)
    return json.jsonify(cartItems)

@app.route('/api/getOrders', methods=['GET'])
def apiGetOrders():
    accessID = int(request.args.get('accessID', default=-1)) #negative id. Probably should use a better way to get the current users id.
    id = int(request.args.get('id', default=-1)) #negative id should not exist
    ordersInfo = get_db().apiGetOrders(accessID, id)
    return json.jsonify(ordersInfo)

@app.route('/api/getAllOrders', methods=['GET'])
def apiGetAllOrders():
    accessID = int(request.args.get('accessID', default=-1)) #negative id. Probably should use a better way to get the current users id.
    ordersInfo = get_db().apiGetAllOrders(accessID)
    return json.jsonify(ordersInfo)

@app.route('/api/addToCart', methods=['POST'])
def apiAddToCart():
    accessID = int(request.args.get('accessID', default=-1)) #negative id. Probably should use a better way to get the current users id.
    id = int(request.args.get('id', default=-1)) #negative id should not exist
    itemID = int(request.args.get('itemID', default=-1)) #negative id should not exist
    count = int(request.args.get('count', default=0))

    result = get_db().apiAddToCart(accessID, id, itemID, count)
    return result

@app.route('/api/addOrder', methods=['POST'])
def apiAddOrder():
    accessID = int(request.args.get('accessID', default=-1)) #negative id. Probably should use a better way to get the current users id.
    id = int(request.args.get('id', default=-1)) #negative id should not exist

    result = get_db().apiAddOrder(accessID, id)
    return result


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/order')
def order():
    return render_template('order.html')

@app.route('/orderHistory')
def orderHistory():
    return render_template('orderHistory.html')

@app.route('/userInfo')
def userInfo():
    return render_template('userInfo.html')


if __name__ == '__main__':
    app.run(host='localhost', port=8080, debug=True)
