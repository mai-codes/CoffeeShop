import os

from datetime import datetime
from flask import Flask, g, json, render_template, request, redirect, session
from passlib.hash import pbkdf2_sha256
from db import Database

app = Flask(__name__)
app.secret_key = b'topsecretkeydontshare!'


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
    userID = -1
    if(session['user'] != None):
        userID = int(session['user']['id']) #can get from the session variable.
    cartItems = get_db().apiGetCart(userID)
    return json.jsonify(cartItems)

@app.route('/api/getOrders', methods=['GET'])
def apiGetOrders():
    accessID = -1
    if(session['user'] != None):
        accessID = int(session['user']['id']) #can get from the session variable.
    userID = int(request.args.get('userID', default=-1)) #negative id should not exist
    ordersInfo = get_db().apiGetOrders(accessID, userID)
    return json.jsonify(ordersInfo)

@app.route('/api/getAllOrders', methods=['GET'])
def apiGetAllOrders():
    accessID = -1
    if(session['user'] != None):
        accessID = int(session['user']['id']) #can get from the session variable.
    ordersInfo = get_db().apiGetAllOrders(accessID)
    return json.jsonify(ordersInfo)

@app.route('/api/getPendingOrders', methods=['GET'])
def apiGetPendingOrders():
    accessID = -1
    if(session['user'] != None):
        accessID = int(session['user']['id']) #can get from the session variable.
    ordersInfo = get_db().apiGetPendingOrders(accessID)
    return json.jsonify(ordersInfo)


# ALL POST METHODS


@app.route('/api/addToCart', methods=['POST'])
def apiAddToCart():
    userID = -1
    if(session['user'] != None):
        userID = int(session['user']['id']) #can get from the session variable.

    itemID = int(request.form.get('itemID', default=-1)) #negative id should not exist
    count = int(request.form.get('count', default=0))

    result = get_db().apiAddToCart(userID, itemID, count)
    return json.jsonify(result)

@app.route('/api/createOrder', methods=['POST'])
def apiCreateOrder():
    userID = -1
    if(session['user'] != None):
        userID = int(session['user']['id']) #can get from the session variable.

    result = get_db().apiCreateOrder(userID)
    return json.jsonify(result)

@app.route('/api/addItem', methods=['POST'])
def apiAddItem():
    accessID = -1
    if(session['user'] != None):
        accessID = int(session['user']['id']) #can get from the session variable.
    itemType = int(request.form.get('itemType', default=0)) #0 == coffee, 1 == tea. Just for sorting purposes
    name = int(request.form.get('name', default='N/A'))
    price = int(request.form.get('price', default=0.00))
    image = int(request.form.get('image', default=''))
    desc = int(request.form.get('description', default=''))
    
    result = get_db().apiAddItem(accessID, itemType, name, price, image, desc)
    return json.jsonify(result)

@app.route('/api/deleteItem', methods=['POST']) #changed to post since delete is not suppose to have a body and jquery does not have $.delete()
def apiDeleteItem():
    accessID = -1
    if(session['user'] != None):
        accessID = int(session['user']['id']) #can get from the session variable.
    id = int(request.form.get('itemID', default=-1)) #negative id should not exist
    result = get_db().apiDeleteItem(accessID, id)
    return json.jsonify(result)

@app.route('/api/approveOrder', methods=['POST'])
def apiApproveOrder():
    accessID = -1
    if(session['user'] != None):
        accessID = int(session['user']['id']) #can get from the session variable.
    orderID = int(request.form.get('orderID', default=-1)) #negative id should not exist
    result = get_db().apiApproveOrder(accessID, orderID)
    return json.jsonify(result)

@app.route('/api/cancelOrder', methods=['POST'])
def apiCancelOrder():
    accessID = -1
    if(session['user'] != None):
        accessID = int(session['user']['id']) #can get from the session variable.
    userID = int(request.form.get('userID', default=-1))
    orderID = int(request.form.get('orderID', default=-1)) #negative id should not exist
    message = int(request.form.get('message', default='User Requested'))
    result = get_db().apiCancelOrder(accessID, userID, orderID, message)
    return json.jsonify(result)

@app.route('/createNewUser', methods=['GET', 'POST'])
def createNewUser():
    message = None
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        typed_password = request.form.get('password')
        user_type = request.form.get('userType')
        if email and username and typed_password and user_type:
            encrypted_password = pbkdf2_sha256.hash(typed_password)
            get_db().create_user(email, username, encrypted_password, user_type)
            return redirect('/login')
        else:
            message = "All fields are required, please try again."
    return render_template('createNewUser.html', message=message)

@app.route('/login', methods=['GET', 'POST'])
def login():
    message = None
    if request.method == 'POST':
        username = request.form.get('username')
        typed_password = request.form.get('password')
        if username and typed_password:
            user = get_db().get_user(username)
            if user:
                if pbkdf2_sha256.verify(typed_password, user["EncryptPass"]):
                    session['user'] = user
                    return redirect('/')
                else:
                    message = "Incorrect password, please try again"
            else:
                message = "Unknown user, please try again"
        else:
            message = "Invalid login, please try again"
    return render_template('login.html', message=message)

@app.route('/logout', methods=['GET'])
def logout():
    #drop session cookie
    session['user'] = None
    #redirect to home
    return redirect('/')
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

@app.route('/cart')
def cart():
    return render_template('cart.html')

@app.route('/test')
def testPage():
    return render_template('test.html')


if __name__ == '__main__':
    app.run(host='localhost', port=8080, debug=True)
