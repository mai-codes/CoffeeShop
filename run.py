from datetime import datetime
from flask import Flask, g, json, jsonify, render_template, request, redirect, session, url_for

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
    userID = None
    if(session.get('user').get('userinfo').get('sub') != None):
        userID = session.get('user').get('userinfo').get('sub') #can get from the session variable.

    cartItems = get_db().apiGetCart(userID)
    return json.jsonify(cartItems)

@app.route('/api/getOrders', methods=['GET'])
def apiGetOrders():
    userID = None
    if(session.get('user').get('userinfo').get('sub') != None):
        userID = session.get('user').get('userinfo').get('sub') #can get from the session variable.

    ordersInfo = get_db().apiGetOrders(userID)
    return json.jsonify(ordersInfo)

# User ID no longer needed here other than to check for permissions which can be done differently.
@app.route('/api/getAllOrders', methods=['GET'])
def apiGetAllOrders():
    ordersInfo = get_db().apiGetAllOrders()
    return json.jsonify(ordersInfo)

# User ID no longer needed here other than to check for permissions which can be done differently.
@app.route('/api/getPendingOrders', methods=['GET'])
def apiGetPendingOrders():

    ordersInfo = get_db().apiGetPendingOrders()
    return json.jsonify(ordersInfo)


# ALL POST METHODS


@app.route('/api/addToCart', methods=['POST'])
def apiAddToCart():
    userID = None
    if(session.get('user').get('userinfo').get('sub') != None):
        userID = session.get('user').get('userinfo').get('sub') #can get from the session variable.

    itemID = int(request.form.get('itemID', default=-1)) #negative id should not exist
    size = request.form.get('size', default="Small")
    count = int(request.form.get('count', default=0))

    result = get_db().apiAddToCart(userID, itemID, size, count)
    return json.jsonify(result)

@app.route('/api/removeFromCart', methods=['POST'])
def apiRemoveFromCart():
    userID = None
    if(session.get('user').get('userinfo').get('sub') != None):
        userID = session.get('user').get('userinfo').get('sub') #can get from the session variable.

    cartItemID = int(request.form.get('cartItemID', default=-1)) #negative id should not exist

    result = get_db().apiRemoveFromCart(userID, cartItemID)
    return json.jsonify(result)

@app.route('/api/createOrder', methods=['POST'])
def apiCreateOrder():
    userID = None
    if(session.get('user').get('userinfo').get('sub') != None):
        userID = session.get('user').get('userinfo').get('sub') #can get from the session variable.

    result = get_db().apiCreateOrder(userID)
    return json.jsonify(result)

# Access ID no longer needed other than to check for permissions which can be done differently.
@app.route('/api/addItem', methods=['POST'])
def apiAddItem():
    
    itemType = int(request.form.get('itemType', default=0)) #0 == coffee, 1 == tea. Just for sorting purposes
    name = str(request.form.get('name', default='N/A'))
    smprice = int(request.form.get('smallprice', default=0.00))
    mdprice = int(request.form.get('mediumprice', default=0.00))
    lgprice = int(request.form.get('largeprice', default=0.00))
    image = str(request.form.get('image', default=''))
    desc = str(request.form.get('description', default=''))
    
    result = get_db().apiAddItem( itemType, name, smprice, mdprice, lgprice, image, desc)
    return json.jsonify(result)

# Access ID no longer needed other than to check for permissions which can be done differently.
@app.route('/api/deleteItem', methods=['POST']) #changed to post since delete is not suppose to have a body and jquery does not have $.delete()
def apiDeleteItem():
    id = int(request.form.get('id', default=-1)) #negative id should not exist
    result = get_db().apiDeleteItem(id)
    return json.jsonify(result)

# Access ID no longer needed other than to check for permissions which can be done differently.
@app.route('/api/approveOrder', methods=['POST'])
def apiApproveOrder():
    orderID = int(request.form.get('orderID', default=-1)) #negative id should not exist
    result = get_db().apiApproveOrder(orderID)
    return json.jsonify(result)

# Access ID no longer needed other than to check for permissions which can be done differently.
@app.route('/api/cancelOrder', methods=['POST'])
def apiCancelOrder():
    userID = None
    if(session.get('user').get('userinfo').get('sub') != None):
        userID = session.get('user').get('userinfo').get('sub') #can get from the session variable.

    orderID = int(request.form.get('orderID', default=-1)) #negative id should not exist
    message = request.form.get('message', default='User Requested')
    result = get_db().apiCancelOrder(userID, orderID, message)
    # print(result)
    return json.jsonify(result)

# Access ID no longer needed other than to check for permissions which can be done differently.
@app.route('/api/cancelOrderAdmin', methods=['POST'])
def apiCancelOrderAdmin():
    orderID = int(request.form.get('orderID', default=-1)) #negative id should not exist
    message = request.form.get('message', default='No Reason Given')
    result = get_db().apiCancelOrder(orderID, message)
    return json.jsonify(result)

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
@requires_auth('get:drinks')
def userInfo(jwt):
    return render_template('userInfo.html', session=session.get('user'), pretty=json.dumps(session.get('user'), indent=4), permission = jwt.get('permissions'))

@app.route('/cart')
def cart():
    return render_template('cart.html', session=session.get('user'), pretty=json.dumps(session.get('user'), indent=4))

@app.route('/barista')
@requires_auth('post:drinks')
def testPage(jwt):
    return render_template('barista.html', session=session.get('user'), pretty=json.dumps(session.get('user'), indent=4), permission = jwt.get('permissions'))

@app.route('/manager', methods=['GET', 'POST'])
@requires_auth('post:drinks')
def manager(jwt):
    if request.method == 'POST':
        apiAddItem()
    return render_template('manager.html', session=session.get('user'), pretty=json.dumps(session.get('user'), indent=4), permission = jwt.get('permissions'))


@app.errorhandler(AuthError)
def handle_auth_error(ex):
    return render_template('errors/401.html'), 401
    

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
