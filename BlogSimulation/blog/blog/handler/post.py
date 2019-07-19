from webob import exc
import datetime
import re
import math

from web import EmulateWeb
from ..model import PostBlog, session, Content, Dig, Tags, BlogTag
from .user import authenticate
from ..util import jsonify

post_router = EmulateWeb.Router('/post')


@post_router.post('/')
@authenticate
def pub(ctx, request:EmulateWeb.Request):
    payload = request.json

    try:
        author_id = request.user.id
        title = payload.get('title')
        text = payload.get('content')
        tags = re.split('[\s,]+',payload.get('tag', ''))
    except:
        raise exc.HTTPBadRequest()
    content = Content()
    content.content = text
    post = PostBlog()
    post.authorid = author_id
    post.title = title
    post.content = content
    post.postdate = datetime.datetime.now()

    for tag in tags:
        t = session.query(Tags).filter(Tags.tag == tag).fist()
        if not t:
            t = Tags()
            t.tag = tag
            session.add(t)

        blog_tag = BlogTag()
        blog_tag.blog = post
        blog_tag.tag = t
        session.add(blog_tag)

    session.add(post)

    try:
        session.commit()
        return jsonify(post_id=post.id)
    except:
        session.rollback()
        raise exc.HTTPInternalServerError

@post_router.get('/{id:int}')
def get(ctx, request:EmulateWeb.Request):
    '''request specific blog'''
    blog_id = request.vars.id
    try:
        blog = session.query(PostBlog).filter(PostBlog.id == blog_id).one()
        print(blog.hits, type(blog.hits))

        blog.hits += 1
        session.add(blog)
        try:
            session.commit()
        except:
            session.rollback()

        #dig_info bury_info
        dig_info, bury_info = get_dig_or_bury(blog_id)

        #tags
        tags = session.query(BlogTag).filter(BlogTag.blog_id == blog_id).limit(10).all()
        if tags:
            tags_info = {[{'tag_id': tag.tag_id, 'tag': tag.tag.tag} for tag in tags]}
        else:
            tags_info = {}

        return jsonify(blog={
            'blog_id':blog.id,
            'title':blog.title,
            'author':blog.author.name,
            'post_date':blog.postdate.timestamp(),
            'content':blog.content.content
        }, dig_info = dig_info, bury_info = bury_info, tags_info=tags_info)
    except Exception as e:
        print(e)
        raise exc.HTTPNotFound()


def get_dig_or_bury(blog_id):
    dig_query = session.query(Dig).filter(Dig.blog_id == blog_id)
    dig_count = dig_query.filter(Dig.state == 1).count()
    dig_list = dig_query.filter(Dig.state == 1).order_by(Dig.putdate.desc()).limit(10).all()
    dig_info = {'count': dig_count, 'users': [{'user_id': dig.user_id, 'name': dig.user.name} for dig in dig_list]}
    bury_count = dig_query.filter(Dig.state == 0).count()
    bury_list = dig_query.filter(Dig.state == 0).order_by(Dig.putdate.desc()).limit(10).all()
    bury_info = {'count': bury_count,
                 'users': [{'user_id': bury.user_id, 'name': bury.user.name} for bury in bury_list]}

    return dig_info, bury_info


def getparam(d:dict, name:str, param_type, default, func):
    result = param_type(d.get(name, default))
    result = func(result, default)
    return result

@post_router.get('/')
@post_router.get('/user/{id:int}')
@post_router.get('/tag/{tag:str}')
def list(ctx, request:EmulateWeb.Request):
    '''query blogs in database, user can set the page and the number of blogs in each page'''

    # try:
    #     page = int(request.params.get('page', 1))
    #     page = page if page > 0 else 1
    # except:
    #     page = 1
    page = getparam(request.params, 'page', int, 1, lambda x,y:x if x>0 else y)
    size = getparam(request.params, 'size', int, 10, lambda x,y:x if x>0 and x<31 else y)

    try:
        count = session.query(PostBlog).count()
        blogs = session.query(PostBlog).order_by(PostBlog.id.desc()).limit(size).offset(size*(page-1)).all()
        return jsonify(blogs=[{
            'blog_id':blog.id,
            'title':blog.title,
        } for blog in blogs],
        page_info={
            'page':page,
            'size':size,
            'count':count,
            'pages':math.ceil(count / size)
        })
    except Exception as e:
        print(e)
        raise exc.HTTPInternalServerError()

def dig_or_bury(userid, blogid, state):
    '''set the state dig or bury on one blog'''
    dig = Dig()
    dig.user_id = userid
    dig.blog_id = blogid
    dig.state = state

    session.add(dig)
    try:
        session.commit()
        return jsonify()
    except:
        session.rollback()
        return jsonify(status=500)

@post_router.put('/dig/{id:int}')
@authenticate
def dig(ctx, request:EmulateWeb.Request):
    '''put the state dig to one blog'''
    return dig_or_bury(request.user.id, request.vars.id, 1)

@post_router.put('/bury/{id:int}')
@authenticate
def bury(ctx, request:EmulateWeb.Request):
    '''put the state bury to one blog'''
    return dig_or_bury(request.user.id, request.vars.id, 0)
