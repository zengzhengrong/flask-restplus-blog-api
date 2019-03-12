from flask import request
from functools import wraps
from blog_api.models import User
from blog_api import bcrypt
from flask_login import login_user,logout_user,current_user
authorization = {
    'apikey':{
        'type':'apiKey',
        'in':'header',
        'name':'DEV-API-KEY'
    }
}
def admin_dev_token_required(f):
    @wraps(f)
    def decorated(*args,**kwargs):
        respon, status = dev_check_token(request)
        data = respon.get('data')
        if not data:
            logout_user() # logout if token invalid
            return respon,status
        if not data.get('admin'):
            permission_respon = {
                'status': 'fail',
                'message': 'you do not have permission!'
            }
            return permission_respon,401
        if not current_user.is_authenticated:
            login_required_respon = {
                'status': 'fail',
                'message': 'please login'
            }
            return login_required_respon,401
        return f(*args,**kwargs)
    return decorated
def dev_token_required(f):
    @wraps(f)
    def decorated(*args,**kwargs):
        respon, status = dev_check_token(request)
        data = respon.get('data')
        if not data:
            logout_user() # logout if token invalid
            return respon,status
        return f(*args,**kwargs)
    return decorated

def token_required(f):
    @wraps(f)
    def decorated(*args,**kwargs):
        respon, status = check_token(request)
        data = respon.get('data')
        if not data:
            return respon,status
        return f(*args,**kwargs)
    return decorated

def login_user_auth(data):
    '''
    Login generate token by user_id 
    '''
    try:   
        email = data.get('email')
        password = data.get('password')
        user = User.query.filter_by(email=email).first()
        
        if not user:
            error_respon = {
                'status': 'fail',
                'message': 'user does not exist'
            }
            return error_respon,404
        check_password = bcrypt.check_password_hash(user.password,password)
        if not check_password:
            error_respon = {
                'status': 'fail',
                'message': 'email or password does not match'
            }
            return error_respon,401
        # user exist and email&password math
        login_user(user)# login by flask-login
        auth_token = User.auth_encode_token(user.id)
        if auth_token:
            success_respon = {
                'status':'success',
                'message':'You Successfully Login',
                'token': auth_token.decode('utf-8')
            }
            return success_respon,200

    except Exception as e:
        error_respon = {
                'status': 'fail',
                'message': e
            }
        return error_respon,500

def logout_user_auth(request):
    '''Logout'''
    dev_token = request.headers.get('DEV-API-KEY')
    pro_token = request.headers.get('Authorization')
    auth_token = None
    if pro_token:
        auth_token = pro_token.split(" ")[1]
    if dev_token:
        auth_token = dev_token
    if auth_token:
        result = User.auth_decode_token(auth_token)
        if isinstance(result,str):
            # token invalid or expired
            error_respon = {
                'status': 'fail',
                'message': result
            }
            return error_respon,401
        # token isvalid ,correct logout
        logout_user() # logout by flask-login
        success_respon = {
                'status': 'success',
                'message': 'You Successfully Logout'
            }
        return success_respon,200
    else:
        error_respon = {
                'status': 'fail',
                'message': 'token does not exist'
            }
        return error_respon,403

def check_token(request):
    '''
    If some methods login required  
    This function would check auth_token before when run login-required methods  
    '''
    auth_token = request.headers.get('Authorization')
    if auth_token:
        result = User.auth_decode_token(auth_token)
        if isinstance(result,str):
        # token invalid or expired
            error_respon = {
                'status': 'fail',
                'message': result
            }
            return error_respon,401
        # token isvalid , get user info
        try:
            user = User.query.get(int(result))
            success_respon = {
                    'status': 'success',
                    'data': {
                        'user_id': user.id,
                        'username': user.username,
                        'active': user.active,
                        'admin': user.admin,
                        'created': user.created_time
                    }
                }
            return success_respon,200
        except Exception as e:
            # get user occur error
            error_respon = {
                'status': 'fail',
                'message': e
            }
            return error_respon,401
    else:
        # auth_token does noe exist
        error_respon = {
            'status': 'fail',
            'message': 'token does no exist, please login'
        }
        return error_respon,401
def dev_check_token(request):
    '''
    For development
    If some methods login required  
    This function would check auth_token before when run login-required methods  
    '''
    auth_token = request.headers.get('DEV-API-KEY')
    if auth_token:
        result = User.auth_decode_token(auth_token)
        if isinstance(result,str):
        # token invalid or expired
            error_respon = {
                'status': 'fail',
                'message': result
            }
            return error_respon,401
        # token isvalid , get user info
        try:
            user = User.query.get(int(result))
            success_respon = {
                    'status': 'success',
                    'data': {
                        'user_id': user.id,
                        'username': user.username,
                        'active': user.active,
                        'admin': user.admin,
                        'created': user.created_time
                    }
                }
            return success_respon,200
        except Exception as e:
            # get user occur error
            error_respon = {
                'status': 'fail',
                'message': e
            }
            return error_respon,401
    else:
        # auth_token does noe exist
        error_respon = {
            'status': 'fail',
            'message': 'token does no exist , please login'
        }
        return error_respon,401




