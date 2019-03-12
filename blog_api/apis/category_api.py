from flask_restplus import Namespace, Resource, fields,abort
from blog_api.models import Category,Post
from blog_api import db
from blog_api.core.authorization import admin_dev_token_required
category_api = Namespace('category',description='category methods')
category_posts = category_api.model('CategoryPostSchema',{
    'url': fields.Url('api.post_single',absolute=True,id='id'),
    'id':fields.Integer(readonly=True,description='The post id'),
    'title':fields.String(readonly=True,description='The post title'),
    'created': fields.DateTime(readonly=True,attribute='created_time'),
    'updated': fields.DateTime(readonly=True,attribute='updated_time')
})

category = category_api.model('CategorySchema',{
    'id':fields.Integer(readonly=True,description='The category id'),
    'name':fields.String(required=True,description='The category name'),
    
})

class PostCount(fields.Raw):
    __schema_example__ = 'auto'
    def format(self,method):
        return method()

# category_with_posts = category_api.inherit('CategoryWithPosts',category,{
#     'posts_count':PostCount(readOnly=True,attribute='posts_count',description='The number of posts by category'),
#     'posts':fields.List(fields.Nested(category_posts,skip_none=True),description='The category posts')
# })
# Same result of above
# This function would push parent fields to first element
def category_with_posts():
    category_with_posts = category_api.inherit('CategoryWithPosts',category)
    category_with_posts['posts_count'] = PostCount(readOnly=True,attribute='posts_count',description='The number of posts by category')
    category_with_posts['posts'] = fields.List(fields.Nested(category_posts,skip_none=True),description='The category posts')
    return category_with_posts

category_with_posts = category_with_posts()

def category_required(field='name'):
    category_required = category_api.clone('CategoryRequiredSchema',category)
    required_value = category_required.pop(field)
    category_required.clear()
    category_required[field] = required_value
    return category_required

category_required = category_required()

@category_api.route('/')

class CategoryList(Resource):
    ''' Show a list of all categorys,and POST a new category'''
    @category_api.doc('list_category')
    @category_api.marshal_list_with(category)
    def get(self):
        '''List of category'''
        categroys = Category.query.all()
        return categroys

    @category_api.doc('create_category')
    @admin_dev_token_required
    @category_api.expect(category_required)
    @category_api.marshal_with(category)
    @category_api.response(400,'Category already existed')
    def post(self):
        '''Create a new category'''
        data = category_api.payload
        category_exist = Category.query.filter_by(name=data['name']).first()
        if category_exist:
            return category_api.abort(400,f'Category({category_exist}) already existed ')
        new_category = Category(name=data['name'])
        db.session.add(new_category)
        db.session.commit()
        return new_category,201

@category_api.route('/<int:id>')
@category_api.response(404,'Category not found')    
class CategorySingle(Resource):
    '''Show a single category item and lets you delete them'''
    @category_api.doc('get_category')
    @category_api.marshal_with(category_with_posts)
    def get(self,id):
        '''Get the category by id'''
        category = Category.query.get(id)
        if not category:
            return abort(404,f'category by id={id} not found')
        return category
    @category_api.doc('delete_category')
    @admin_dev_token_required
    @category_api.response(204,'Category deleted')    
    def delete(self,id):
        '''Delete the category by id'''
        category = Category.query.get(id)
        if not category:
            return abort(404,f'category by id={id} not found')
        db.session.delete(category)
        db.session.commit()
        return {'messgae':f'category({category.name}) deleted'}
    @category_api.doc('update_category')
    @admin_dev_token_required
    @category_api.expect(category_required)
    @category_api.marshal_with(category_with_posts)
    def put(self,id):
        '''Update the category by id'''
        category = Category.query.get(id)
        if not category:
            return abort(404,f'category by id={id} not found')
        data = category_api.payload
        category.name = data.get('name')
        db.session.commit()
        return category


        
