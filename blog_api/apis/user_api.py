import uuid
from blog_api import bcrypt,db
from flask_restplus import Namespace,Resource,fields
from blog_api.models import User
from .category_api import category_posts
from blog_api.core.utils import CreateApiModel
from blog_api.core.authorization import admin_dev_token_required,authorization

user_api = Namespace('user',description='user methods')

user_posts = user_api.inherit('UserPostSchema',category_posts)

user = user_api.model('UserSchema',{
    'id': fields.Integer(readonly=True,description='The user id'),
    'public_id': fields.String(readonly=True,description='The user public_id'),
    'username': fields.String(readonly=True,description='The user username'),
    'email' : fields.String(required=True, description='The user email address'),
    'active':fields.Boolean(readonly=True,description='The user is active'),
    'admin': fields.Boolean(readonly=True,description='The user is admin'),
    'created': fields.DateTime(readonly=True,attribute='created_time'),
    'avatar': fields.String(attribute='image_file',readonly=True,description='The user avatar image'),
    'posts': fields.List(fields.Nested(user_posts,skip_none=True,description='The user posts'))
    
})

new_model = CreateApiModel(user_api,user,'UserSingleSchema')
user_single = new_model.inherit_remove(remove_list=['id','active','admin'])

signup_required = user_api.model('SignupSchema',{
    'username': fields.String(required=True,description='The user username'),
    'email' : fields.String(required=True, description='The user email address'),
    'password': fields.String(required=True, description='The user password')
})
superuser_permission_model = user_api.model('SuperSchema',{
    'email' : fields.String(required=True, description='The user email address'),
    'active':fields.Boolean(required=True,description='The user is active'),
    'admin': fields.Boolean(required=True,description='The user is admin'),
    'avatar': fields.String(required=True,attribute='image_file',description='The user avatar image'),
})
# api view 
@user_api.route('/')
class UserList(Resource):
    '''Shows a list of all users, and lets you POST to add new user'''

    @user_api.doc('list_user')
    @admin_dev_token_required
    @user_api.marshal_list_with(user)
    def get(self):
        '''List all user'''
        users = User.query.all()
        return users

    @user_api.doc('create_user')
    @user_api.response(201,'User create success')
    @user_api.expect(signup_required)
    def post(self):
        '''Create a new user'''
        data = user_api.payload
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        is_exist_email = User.query.filter_by(email=email).first()
        is_exist_username = User.query.filter_by(username=username).first()
        if is_exist_email:
            error_respon = {
                'status':'fail',
                'message': 'User by email already exists, Please reset'
            }
            return error_respon,409
        if is_exist_username:
            error_respon = {
                'status':'fail',
                'message': 'User by username already exists, Please rename'
            }
            print(1)
            return error_respon,409
        password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(public_id=str(uuid.uuid4()),email=email,username=username,password=password_hash)
        db.session.add(new_user)
        db.session.commit()
        success_respon = {
            'status':'success',
            'message': 'User signup success, Please login'
        }
        return success_respon,201


@user_api.route('/<public_id>')
@user_api.response(404,'User not found')
class UserSingle(Resource):
    '''Show single user and let delete put'''

    @user_api.doc('get_user')
    @user_api.marshal_with(user_single)
    def get(self,public_id):
        '''Get user by public_id'''
        user = User.query.filter_by(public_id=public_id).first()
        print(user)
        if not user:
            return user_api.abort(404,'User not found')
        return user

    @user_api.doc('delete_user')
    @admin_dev_token_required
    @user_api.response(204,'user deleted')
    def delete(self,public_id):
        '''Delete user by public_id'''
        user = User.query.filter_by(public_id=public_id).first()
        if not user:
            return user_api.abort(404,'User not found')
        db.session.delete(user)
        db.session.commit()
        return {'messgae':f'{user} deleted'},204

    @user_api.doc('update_user')
    @admin_dev_token_required
    @user_api.expect(superuser_permission_model)
    @user_api.marshal_with(user_single)
    def put(self,public_id):
        '''Update user by public_id'''
        user = User.query.filter_by(public_id=public_id).first()
        if not user:
            return user_api.abort(404,'User not found')
        data = user_api.payload
        active = data.get('active')
        admin = data.get('admin')
        user.active = active
        user.admin = admin
        db.session.commit()
        return user
