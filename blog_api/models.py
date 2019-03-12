import jwt
from blog_api import db,login_manager
from datetime import datetime,timedelta
from flask_login import UserMixin
from blog_api.config import key


@login_manager.user_loader
def loader_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    public_id = db.Column(db.String(100), unique=True,nullable=False)
    username = db.Column(db.String(12),unique=True,nullable=False)
    email = db.Column(db.String(20),unique=True,nullable=False)
    password = db.Column(db.String(60),nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    active = db.Column(db.Boolean,nullable=False,default=True)
    image_file = db.Column(db.String(20),nullable=True,default='default.jpg')
    posts = db.relationship('Post',backref='author',lazy=True)
    created_time = db.Column(db.DateTime,nullable=False,default=datetime.now())
    def __repr__(self):
        return f"User('{self.username}','{self.email}',active:'{self.active}')"
    
    @staticmethod
    def auth_encode_token(user_id):
        ''' Generate token to auth'''
        data = {
            'user_id': user_id,
            'exp':datetime.utcnow() + timedelta(minutes=30),
            'iat':datetime.utcnow() # issued at
        }
        return jwt.encode(data,key)

    @staticmethod    
    def auth_decode_token(auth_token):
        '''Decode token'''
        try:
            data = jwt.decode(auth_token,key)
            return data['user_id']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token.'
            
class Category(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100),nullable=False,unique=True)
    posts = db.relationship('Post',backref='category',lazy=True)
    def __repr__(self):
        return f'Category({self.name})'
    def posts_count(self):
        return len(self.posts)

class Post(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(100),nullable=False)
    body = db.Column(db.Text(),nullable=False)
    created_time = db.Column(db.DateTime,nullable=False,default=datetime.now())
    updated_time = db.Column(db.DateTime,nullable=True)
    post_image = db.Column(db.String(20),nullable=True,default='default.jpg')
    author_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    categroy_id = db.Column(db.Integer,db.ForeignKey('category.id'),nullable=False)
    def __repr__(self):
        return f"Post('{self.title}','{self.categroy_id}')"

