import os

from flask import Flask, g, json, render_template, request
from db import Database

app = Flask(__name__)

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


# ALL GET METHODS

@app.route('/api/getItems', methods=['GET'])
def apiGetItems():
    n = int(request.args.get('n', default=20)) #Assuming that we don't have enough drinks to need more than one page
    offset = int(request.args.get('offset', default=0))
    items = get_db().apiGetItems(n, offset)
    return json.jsonify(items)

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

@app.route('/api/getPendingOrders', methods=['GET'])
def apiGetPendingOrders():
    accessID = int(request.args.get('accessID', default=-1)) #negative id. Probably should use a better way to get the current users id.
    ordersInfo = get_db().apiGetPendingOrders(accessID)
    return json.jsonify(ordersInfo)


# ALL POST METHODS


@app.route('/api/addToCart', methods=['POST'])
def apiAddToCart():
    accessID = int(request.form.get('accessID', default=-1)) #negative id. Probably should use a better way to get the current users id.
    id = int(request.form.get('id', default=-1)) #negative id should not exist
    itemID = int(request.form.get('itemID', default=-1)) #negative id should not exist
    count = int(request.form.get('count', default=0))

    result = get_db().apiAddToCart(accessID, id, itemID, count)
    return json.jsonify(result)

@app.route('/api/createOrder', methods=['POST'])
def apiCreateOrder():
    accessID = int(request.form.get('accessID', default=-1)) #negative id. Probably should use a better way to get the current users id.
    id = int(request.form.get('id', default=-1)) #negative id should not exist

    result = get_db().apiCreateOrder(accessID, id)
    return json.jsonify(result)

@app.route('/api/addItem', methods=['POST'])
def apiAddItem():
    accessID = int(request.form.get('accessID', default=-1)) #negative id. Probably should use a better way to get the current users id.
    itemType = int(request.form.get('itemType', default=0)) #0 == coffee, 1 == tea. Just for sorting purposes
    name = int(request.form.get('name', default='N/A'))
    price = int(request.form.get('price', default=0.00))
    image = int(request.form.get('image', default=''))
    desc = int(request.form.get('description', default=''))
    
    result = get_db().apiAddItem(accessID, itemType, name, price, image, desc)
    return json.jsonify(result)

@app.route('/api/deleteItem', methods=['POST']) #changed to post since delete is not suppose to have a body and jquery does not have $.delete()
def apiDeleteItem():
    accessID = int(request.form.get('accessID', default=-1)) #negative id. Probably should use a better way to get the current users id.
    id = int(request.form.get('itemID', default=-1)) #negative id should not exist
    result = get_db().apiDeleteItem(accessID, id)
    return json.jsonify(result)

@app.route('api/approveOrder', methods=['POST'])
def apiApproveOrder():
    accessID = int(request.form.get('accessID', default=-1)) #negative id. Probably should use a better way to get the current users id.
    orderID = int(request.form.get('orderID', default=-1)) #negative id should not exist
    result = get_db().apiApproveOrder(accessID, orderID)
    return json.jsonify(result)

@app.route('api/cancelOrder', methods=['POST'])
def apiCancelOrder():
    accessID = int(request.form.get('accessID', default=-1)) #negative id. Probably should use a better way to get the current users id.
    userID = int(request.form.get('userID', default=-1))
    orderID = int(request.form.get('orderID', default=-1)) #negative id should not exist
    message = int(request.form.get('message', default='User Requested'))
    result = get_db().apiCancelOrder(accessID, userID, orderID, message)
    return json.jsonify(result)

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

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/createNewUser')
def createNewUser():
    return render_template('createNewUser.html')

@app.route('/test')
def testPage():
    return render_template('test.html')


if __name__ == '__main__':
    app.run(host='localhost', port=8080, debug=True)
