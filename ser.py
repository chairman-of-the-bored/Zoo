import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.escape
import os

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")

class BaseStaticHandler(tornado.web.StaticFileHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")

class NoCacheStaticFileHandler(BaseStaticHandler):


    def set_extra_headers(self, path):
        self.set_header("Cache-control", "no-cache")

class MainHandler(BaseHandler):
    def get(self):
        if not self.current_user:
            self.redirect("/login")
            return
        name = tornado.escape.xhtml_escape(self.current_user)
        self.write("Hello, " + name)

class LoginHandler(BaseHandler):
    def get(self):
        self.write('<html><body><form action="/login" method="post">'
                   'Key: <input type="text" name="key">'
                   '<input type="submit" value="Zoo">'
                   '</form></body></html>')

    def post(self):
        key = self.get_argument("key")
        if key == "5f4dcc3b5aa765d61d8327deb882cf99":
            self.set_secure_cookie("user",key)
            self.redirect("/web/index.html")

class EchoWebSocket(tornado.websocket.WebSocketHandler):
    def open(self):
        print("WebSocket opened")

    def on_message(self, message):
        print(message)
        self.write_message(u"You said: " + message)

    def on_close(self):
        print("WebSocket closed")

    def check_origin(self, origin):
        return True

settings = {
    "cookie_secret": "eb3d3479662ba522936ec994d8202bc5",
    "login_url": "/login",
}

static_path = os.path.join(os.path.dirname(__file__), "web")
image_path = os.path.join(os.path.dirname(__file__), "web", "images")
application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/login", LoginHandler),
    (r"/soc", EchoWebSocket),
    (r"/web/(.*)", NoCacheStaticFileHandler, {"path": static_path}),
    (r"/web/images/(.*)", NoCacheStaticFileHandler, {"path": image_path}),
], **settings)


if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.current().start()