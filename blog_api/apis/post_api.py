from datetime import datetime
from flask import request
from flask_restplus import Namespace, Resource, fields,abort,reqparse
from blog_api.models import Post,Category
from blog_api import db
from six import string_types 
from blog_api.core.authorization import dev_token_required,admin_dev_token_required
from flask_login import current_user

# namespace
post_api = Namespace('post', description='post methods')
# api resource model
post = post_api.model('PostSchema', {
    'id': fields.Integer(readonly=True, description='The post id'),
    'category': fields.String(required=True,attribute='category.name',description='The category name'),
    'title': fields.String(required=True, description='The title name'),
    'body': fields.String(required=True, description='The content body'),
    'created': fields.DateTime(readonly=True,attribute='created_time',example='auto'),
    'updated': fields.DateTime(readonly=True,attribute='updated_time',skip_none=True,example='auto')
})
def post_required(remove_list=['id','created','updated']):
    post_required = post_api.clone('PostRequiredSchema',post)
    for k in remove_list:
        del post_required[k]
    return post_required
post_required = post_required()

# per page of posts
# These key name are mapping attr in Model.query.paginate()
pagination = post_api.model('PaginationSchema', {
    'page': fields.Integer(description='Current Page'),
    'pages': fields.Integer(description='Total number of pages'),
    'per_page': fields.Integer(description='Per page of results'),
    'total': fields.Integer(description='Total results'),
})

perpage_of_posts = post_api.inherit('PerpageSchema',pagination,{
    'items': fields.List(fields.Nested(post))
})
pagination_arguments = reqparse.RequestParser()
pagination_arguments.add_argument('page', type=int, required=False, default=1, help='Page number')
pagination_arguments.add_argument('bool', type=bool, required=False, default=True, help='Page number')
pagination_arguments.add_argument('per_page', type=int, required=False, choices=[2, 10, 20, 30, 40, 50],
                                  default=10, help='Results per page {error_msg}')

# views
@post_api.route('/')
class PostList(Resource):
    '''Shows a list of all posts, and lets you POST to add new post'''
    @post_api.doc('list_post')
    @post_api.expect(pagination_arguments,validate=True)
    @post_api.marshal_list_with(perpage_of_posts)
    def get(self):
        '''List all posts'''
        args = pagination_arguments.parse_args(request)
        page = args.get('page',1)
        per_page = args.get('per_page', 10)
        posts = Post.query.paginate(page, per_page, error_out=False)
        return posts
    @post_api.doc('create_post')
    @admin_dev_token_required
    @post_api.expect(post_required)
    @post_api.marshal_with(post, code=201,skip_none=True)
    def post(self):
        '''Create a new post'''
        data = post_api.payload
        print(data)
        category = Category.query.filter_by(name=data['category']).first()
        if not category:
            return abort(404,'category not found')
        new_post = Post(category=category,title=data['title'],body=data['body'],author=current_user)
        print(new_post)
        db.session.add(new_post)
        db.session.commit()
        return new_post, 201


@post_api.route('/<int:id>',endpoint='post_single')
@post_api.response(404, 'Post not found')
@post_api.param('id', 'The post identifier')
class PostSingle(Resource):
    '''Show a single post item and lets you delete them'''
    @post_api.doc('get_post')
    @post_api.marshal_with(post,skip_none=True)
    def get(self, id):
        '''Get the post by id'''
        post = Post.query.get(id)
        if not post:
            return abort(404,f'post by id={id} not found')
        return post

    @post_api.doc('delete_post')
    @admin_dev_token_required
    @post_api.response(204, 'Post deleted')
    def delete(self, id):
        '''Delete the post by id'''
        post = Post.query.get(id)
        if not post:
            return abort(404,f'post by id={id} not found')
        db.session.delete(post)
        db.session.commit()
        return {'messgae':f'post({post.title}) deleted'}

    @post_api.doc('update_post')
    @admin_dev_token_required
    @post_api.expect(post_required)
    @post_api.marshal_with(post)
    def put(self, id):
        '''Update the post by id'''
        data = post_api.payload
        post = Post.query.get(id)
        if not post:
            return abort(404,f'post by id={id} not found',post='update fail')
        post.title = data['title']
        post.body = data['body']
        post.updated_time = datetime.now()
        db.session.commit()
        return post