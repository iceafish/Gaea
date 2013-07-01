#!/usr/bin/env python

import tornado.web
import tornado.httpserver
import tornado.options
import tornado.ioloop
import tornado.auth
import os.path
import pymongo
import subprocess
from tornado.options import define, options
from admin import *
from problems import *
from users import *

define("port", default=8888, help="run on the given port", type=int)

class Application(tornado.web.Application):
    
    def __init__(self):
        handlers = [
            (r"/", IndexHandler),
            (r"/problems", ProblemsHandler),
            (r"/problem/(\d+)", ShowProblemHandler),
            (r"/status", StatusHandler),
            (r"/status/(\d+)", ComplieErrInfoHandler),
            (r"/ranklist", RankHandler),
            (r"/submit/(\d+)", SubmitProblemHandler),
            
            (r"/faq", FaqHandler),

            (r"/user/(\w+)", UserInfoHandler),

            (r"/register", RegisterUserHandler),
            (r"/login", UserLoginHandler),
            (r"/logout", UserLogoutHandler),
            
            (r"/admin", AdminHomeHandler),
            (r"/admin/login", AdminLoginHandler),
            (r"/admin/logout", AdminLogoutHandler),
            (r"/admin/add/problem", AddProblemHandler),
            (r"/admin/add/data", AddDataFileIndexHandler),
            (r"/admin/add/data/(\d+)", AddDataFileHandler),
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
        return self.get_secure_cookie("user_info")
    
    def get(self):
        if self.current_user:
            name = self.current_user
        else:
            name = "None"
        self.render("index.html", curuser = name)
        
        
class StatusHandler(tornado.web.RequestHandler):
    
    def get(self):
        db = self.application.db.judge_queues
        self.render("status.html", status_list=db.find().sort('_id',-1).limit(10))

class ComplieErrInfoHandler(tornado.web.RequestHandler):

    def get(self, id):
        db = self.application.db.judge_queues.find_one({'_id':int(id)})

        if not db or not db['result']['err_code']:
            return self.write('404, id not exist')

        self.render('error_msg.html', msg=db['result']['err_code'])


class RankHandler(tornado.web.RequestHandler):
    
    def get(self):
        db = self.application.db.users
        self.render("rank.html", users = db.find({'group':'student'}))
        

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