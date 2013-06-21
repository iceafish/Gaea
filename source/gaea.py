#!/usr/bin/env python

import tornado.web
import tornado.httpserver
import tornado.options
import tornado.ioloop
import tornado.auth
import os.path
import pymongo
from tornado.options import define, options
from admin import (AdminHomeHandler, 
                   AddProblemHandler, 
                   AdminLoginHandler,
                   AdminLogoutHandler,)
from problems import (ProblemsHandler, 
                      ShowProblemHandler)
from users import (RegisterUserHandler,
                   UserLoginHandler,
                   UserLogoutHandler)

define("port", default=8888, help="run on the given port", type=int)

class Application(tornado.web.Application):
    
    def __init__(self):
        handlers = [
            (r"/", IndexHandler),
            (r"/problems", ProblemsHandler),
            (r"/problem/(\d+)", ShowProblemHandler),
            (r"/faq", FaqHandler),
            
            (r"/register", RegisterUserHandler),
            (r"/login", UserLoginHandler),
            (r"/logout", UserLogoutHandler),
            
            (r"/admin", AdminHomeHandler),
            (r"/admin/login", AdminLoginHandler),
            (r"/admin/logout", AdminLogoutHandler),
            (r"/admin/add/problem", AddProblemHandler),
        ]
        settings = {
            "template_path" : os.path.join(os.path.dirname(__file__), "templates"),
            "static_path" : os.path.join(os.path.dirname(__file__), "static"),
            "cookie_secret" : "123456789",
            "login_url" : "/",
            "debug" : True,
        }
        conn = pymongo.Connection("localhost", 27017)
        self.db = conn["Gaea"]
        tornado.web.Application.__init__(self, handlers, **settings)


        
class IndexHandler(tornado.web.RequestHandler):
    
    def get_current_user(self):
        return self.get_secure_cookie("userinfo")
    
    def get(self):
        if self.current_user:
            name = self.current_user
        else:
            name = "None"
        self.render("index.html", curuser = name)
        
class FaqHandler(tornado.web.RequestHandler):
    
    def get(self):
        self.render("faq.html")
        
def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
    
if __name__ == "__main__":
    main()