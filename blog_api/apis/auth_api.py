from flask import request
from flask_restplus import Namespace, Resource ,fields
from blog_api.core.authorization import login_user_auth,logout_user_auth

auth_api = Namespace('auth',description='auth methods')

login = auth_api.model('AuthSchema',{
    'email': fields.String(required=True,description='The email address'),
    'password': fields.String(required=True,description='The user password')
})

@auth_api.route('/login')
class Login(Resource):
    '''User login'''

    @auth_api.doc('user_login')
    @auth_api.expect(login)
    def post(self):
        data = auth_api.payload
        return login_user_auth(data)

@auth_api.route('/logout')
class Logout(Resource):
    '''User logout'''

    @auth_api.doc('user_logout')
    def post(self):
        return logout_user_auth(request)



