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
