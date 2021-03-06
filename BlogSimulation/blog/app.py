from wsgiref.simple_server import make_server
from blog import config
from web import EmulateWeb
from blog.handler.user import user_router
from blog.handler.post import post_router

if __name__ == '__main__':
    application = EmulateWeb()
    application.register(user_router)
    application.register(post_router)

    server = make_server(config.WSIP, config.WSPORT, application)
    try:
        server.serve_forever()
    except:
        server.shutdown()
        server.server_close()
