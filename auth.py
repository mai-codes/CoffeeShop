import json
from flask import request, _request_ctx_stack, abort
from functools import wraps
from jose import jwt
from urllib.request import urlopen


AUTH0_DOMAIN = 'dev-u47j7bisvynaztjd.us.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'coffee'
AUTH0_CLIENT_ID = 'UYCUyUXE0ryIUN5ikMM0N0yi107p8cPb'
APP_SECRET_KEY = '2b6a2a8ecf602d54cfa04724db687d7e9d5fb50f42ec9c7897ff3ae1631ca151'

## AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


## Auth Header

def get_token_auth_header():
    # obtain token from authorization header
    # auth = request.headers.get('Authorization', None)
    # print("REQUEST HEADERS: \n", request.headers)
    # print(auth)

    tokenData = open('token.txt', 'r')
    tokenLine = tokenData.readlines()

    token = tokenLine
    auth = ''.join(token)
    # print(auth)
    # check if authorization header included
    if not auth:
        raise AuthError({
            'code': 'authorization_header_missing',
            'description': 'Expected to include Authorization Header'
        }, 401)
    return auth


def check_permissions(permission, payload):
    if ('permissions' not in payload):
        raise AuthError({
            'code': 'invalid_permissions',
            'description': 'User does not have enough privileges'
        }, 400)

    if permission not in payload['permissions']:
        raise AuthError({
            'code': 'unauthorized',
            'description': 'User does not have any roles attached'
        }, 403)

    return True


def verify_decode_jwt(token):
    # Receives the public key from AUTH0
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())

    # get the data in header
    unverified_header = jwt.get_unverified_header(token)

    # select our key
    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError(
            {
                'code': 'invalid_header',
                'description': 'Authorization malformed.'
            }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    # verify key
    if rsa_key:
        try:
            payload = jwt.decode(token,
                                 rsa_key,
                                 algorithms=ALGORITHMS,
                                 audience=API_AUDIENCE,
                                 issuer='https://' + AUTH0_DOMAIN + '/')

            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError(
                {
                    'code': 'token_expired',
                    'description': 'Token expired.'
                }, 401)

        except jwt.JWTClaimsError:
            raise AuthError(
                {
                    'code':
                    'invalid_claims',
                    'description': 'Incorrect claims. Please, check the audience and issuer.'
                }, 401)
        except Exception:
            raise AuthError(
                {
                    'code': 'invalid_header',
                    'description': 'Unable to parse authentication token.'
                }, 400)
    raise AuthError(
        {
            'code': 'invalid_header',
            'description': 'Unable to find the appropriate key.'
        }, 400)


def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)                
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator