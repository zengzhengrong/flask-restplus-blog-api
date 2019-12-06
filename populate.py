from blog_api.models import Category,Post,User
from blog_api import create_app,db,bcrypt
import random
import uuid
app = create_app()
app.app_context().push()
posts = [
'C++',
'C#',
'C',
'Python',
'Java',
'go',
'ruby',
'shell',
'JavaScript',
'html5',
'css5',
'php',
'R',
'MATLAB',
'Perl',
'Objective-C',
'VB',
'sql',
'Swift',
'Lisp',
'Pascal',
'Ruby',
'SAS',
'Erlang',
'OpenCL',
'APL',
'AutoIt',
'BASIC',
'Eiffel',
'Forth',
'Frink',
'ICI',
'Lisp',
'Lua',
'Pascal'
]
users = [
    {
    'username':'admin',
    'email':'admin@163.com',
    'password':'admin'
    },
    {
    'username':'zzr',
    'email':'zzr@163.com',
    'password':'zzr'
    },
    {
    'username':'jianbing',
    'email':'506862754@163.com',
    'password':'jianbing'
    }   
]
categorys =[
    'c1',
    'c2',
    'c3',
    'c4',
    'c5'
]
def cut_post(posts,n):
    for i in range(0,len(posts),n):
        yield posts[i:i+n]
def yield_category():
    for c_name in categorys:
        yield c_name
def populte():
    print('drop database')
    db.drop_all()
    print('drop done')
    print('create database')
    db.create_all()
    print('create database done')
    print('creating......')
    for user in users:
        hash_password = bcrypt.generate_password_hash(user.get('password')).decode('utf-8')
        create_user = User(public_id=str(uuid.uuid4()),username=user.get('username'),email=user.get('email'),password=hash_password,admin=True)
        db.session.add(create_user)
        print('create user success')
    print('create users done')
    admin = User.query.filter_by(username='admin').first()

    per_c = int(len(posts)/len(categorys))
    mod_post = len(posts)%len(categorys)
    print(per_c)
    print(mod_post)
    rm_list = []
    if mod_post != 0:
        for i in range(mod_post):
            rm_index = random.randint(0,len(posts)-1)
            rm_obj = posts.pop(rm_index)
            rm_list.append(rm_obj)
    if rm_list:
        null_category = Category(name='null')
        db.session.add(null_category)
        for post in rm_list:
            create_post = Post(title=post,body=post*3,category=null_category)
            db.session.add(create_post)
    cp = cut_post(posts,per_c)
    cc = yield_category()
    for cut_posts in cp:
        print(cut_posts)
        for c_name in cc:
            print(c_name)
            create_category = Category(name=c_name)
            db.session.add(create_category)
            for post in cut_posts:
                create_post = Post(title=post,body=post*3,category=create_category,author=admin)
                db.session.add(create_post)
                print('create post success')
            break
    db.session.commit()
    print('done')  

if __name__ == '__main__':
    populte()
    