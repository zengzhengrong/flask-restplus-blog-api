from flask import Blueprint
from flask_restplus import Api
from .post_api import post_api
from .category_api import category_api
from .user_api import user_api
from .auth_api import auth_api
from blog_api.core.authorization import authorization
blueprint = Blueprint('api',__name__)
api = Api(blueprint,version='1.0',description='This is a zzr Blog',authorizations=authorization, security='apikey')
api.add_namespace(auth_api)
api.add_namespace(user_api)
api.add_namespace(post_api)
api.add_namespace(category_api)
