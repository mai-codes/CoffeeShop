import json
from functools import wraps
from jose import jwt
from urllib.request import urlopen
from os import environ as env
from dotenv import find_dotenv, load_dotenv

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)
    
'''
Code adapted from Auth0 documentation/github repo:
https://github.com/auth0-samples/auth0-python-api-samples/blob/master/00-Starter-Seed/server.py
'''
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


## Auth Header

def get_token_auth_header():
    tokenData = open('token.txt', 'r')
    tokenLine = tokenData.readlines()

    token = tokenLine
    auth = ''.join(token)

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
    jsonurl = urlopen(f'https://{env.get("AUTH0_DOMAIN")}/.well-known/jwks.json')
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
                                 algorithms=env.get("ALGORITHMS"),
                                 audience=env.get("API_AUDIENCE"),
                                 issuer='https://' + env.get("AUTH0_DOMAIN") + '/')

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