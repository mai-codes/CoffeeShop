from datetime import datetime
from flask import Flask, g, json, jsonify, render_template, request, redirect, session, url_for
from flask_cors import cross_origin

from db import Database
from auth import AuthError, requires_auth
from dotenv import find_dotenv, load_dotenv
from os import environ as env
from authlib.integrations.flask_client import OAuth
from urllib.parse import quote_plus, urlencode

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

app = Flask(__name__)
app.secret_key = env.get("APP_SECRET_KEY")

oauth = OAuth(app)

oauth.register(
    "auth0",
    client_id=env.get("AUTH0_CLIENT_ID"),
    client_secret=env.get("AUTH0_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{env.get("AUTH0_DOMAIN")}/.well-known/openid-configuration'
)

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

# @app.route('/createNewUser', methods=['GET', 'POST'])
# def createNewUser():
#     message = None
#     if request.method == 'POST':
#         email = request.form.get('email')
#         username = request.form.get('username')
#         typed_password = request.form.get('password')
#         user_type = request.form.get('userType')
#         if email and username and typed_password and user_type:
#             encrypted_password = pbkdf2_sha256.hash(typed_password)
#             get_db().create_user(email, username, encrypted_password, user_type)
#             return redirect('/login')
#         else:
#             message = "All fields are required, please try again."
#     return render_template('createNewUser.html', message=message)

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     message = None
#     if request.method == 'POST':
#         username = request.form.get('username')
#         typed_password = request.form.get('password')
#         if username and typed_password:
#             user = get_db().get_user(username)
#             if user:
#                 if pbkdf2_sha256.verify(typed_password, user["EncryptPass"]):
#                     session['user'] = user
#                     return redirect('/')
#                 else:
#                     message = "Incorrect password, please try again"
#             else:
#                 message = "Unknown user, please try again"
#         else:
#             message = "Invalid login, please try again"
#     return render_template('login.html', message=message)

# @app.route('/logout', methods=['GET'])
# def logout():
#     #drop session cookie
#     session['user'] = None
#     #redirect to home
#     return redirect('/')

@app.route("/login")
def login():
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("callback", _external=True),
         audience='coffee'
    )

@app.route("/callback", methods=["GET", "POST"])
def callback():
    token = oauth.auth0.authorize_access_token()
    access = token.get('access_token', None)
    text_file = open("token.txt", "w")
    text_file.write(access)
    text_file.close()
    # print(access)
    session["user"] = token
    return redirect("/")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(
        "https://" + env.get("AUTH0_DOMAIN")
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": url_for("home", _external=True),
                "client_id": env.get("AUTH0_CLIENT_ID"),
            },
            quote_via=quote_plus,
        )
    )

    
@app.route('/')
def home():
    return render_template('home.html', session=session.get('user'), pretty=json.dumps(session.get('user'), indent=4))

@app.route('/order')
def order():
    return render_template('order.html', session=session.get('user'), pretty=json.dumps(session.get('user'), indent=4))

@app.route('/orderHistory')
def orderHistory():
    return render_template('orderHistory.html', session=session.get('user'), pretty=json.dumps(session.get('user'), indent=4))

@app.route('/userInfo')
def userInfo():
    return render_template('userInfo.html', session=session.get('user'), pretty=json.dumps(session.get('user'), indent=4))

@app.route('/cart')
def cart():
    return render_template('cart.html', session=session.get('user'), pretty=json.dumps(session.get('user'), indent=4))

@app.route('/barista')
@requires_auth('post:drinks')
def testPage(jwt):
    return render_template('barista.html', session=session.get('user'), pretty=json.dumps(session.get('user'), indent=4))

@app.route('/manager', methods=['GET', 'POST'])
def manager():
    if request.method == 'POST':
        name = request.form.get('name')
        price = request.form.get('price')
        image = request.form.get('image')
        itemType = request.form.get('type')
        description = request.form.get('description')
        get_db().apiAddItem(accessID=1,itemType= itemType,itemName=name, itemPrice=price,
                                    itemImage=image, itemDescription=description)
    return render_template('manager.html', session=session.get('user'), pretty=json.dumps(session.get('user'), indent=4))



@app.errorhandler(AuthError)
def handle_auth_error(ex):
    return jsonify({
        "success": False,
        "error": ex.status_code,
        'message': ex.error
    }), 401

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
