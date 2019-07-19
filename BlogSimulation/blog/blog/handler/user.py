from webob import exc
import bcrypt
import jwt
import datetime
from web import EmulateWeb
from ..util import jsonify
from .. import config
from ..model import User, session


user_router = EmulateWeb.Router('/user')

def get_token(user_id):
    return jwt.encode({'user_id':user_id,
                       'timestamp':int(datetime.datetime.now().timestamp())}, config.AUTH_SECRET, algorithm='HS256').decode()

@user_router.post('/reg')
def register(ctx, request:EmulateWeb.Request):
    payload = request.json
    print(payload)
    email = payload.get('email')
    if session.query(User).filter(User.email == email).first() is not None:
        raise exc.HTTPConflict('{} is already exist'.format(email))

    user = User()
    try:
        user.name = payload.get('name')
        user.email = payload['email']
        user.password = bcrypt.hashpw(payload['password'].encode(), bcrypt.gensalt())
    except Exception as e:
        print(e)
        raise exc.HTTPBadRequest

    session.add(user)
    try:
        session.commit()
        return jsonify(token=get_token(user.id))
    except:
        session.rollback()
        raise  exc.HTTPServerError


@user_router.post('/login')
def login(ctx, request:EmulateWeb.Request):
    payload = request.json
    email = payload.get('email')
    user = session.query(User).filter(User.email == email).first()
    if user and bcrypt.checkpw(payload.get('password').encode(), user.password.encode()):
        return jsonify(user={
            'id':user.id,
            'name':user.name,
            'email':user.email
        }, token=get_token(user.id))
    else:
        raise exc.HTTPUnauthorized


#token过期判断
def authenticate(fn):
    def wappers(ctx, request:EmulateWeb.Request):
        try:
            jwtstr = request.headers.get('Jwt')
            payload = jwt.decode(jwtstr, config.AUTH_SECRET, algorithms=['HS256'])
            now = datetime.datetime.now().timestamp()
            time = payload.get('timestamp', 0)
            if (now - time) > config.AUTH_EXPIRE: #过期
                print(now)
                print(time)
                raise exc.HTTPUnauthorized

            user = session.query(User).filter(User.id == payload.get('user_id', -1)).first()
            if user is None:
                raise exc.HTTPUnauthorized
            request.user = user
        except Exception as e:
            print(e)
            raise  exc.HTTPUnauthorized
        return fn(ctx, request)
    return wappers










