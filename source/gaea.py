#!/usr/bin/env python

import tornado.web
import tornado.httpserver
import tornado.options
import tornado.ioloop
import os.path
import pymongo
from tornado.options import define, options
from admin import AdminHandler
from Problems import ProblemsHandler

define("port", default=8888, help="run on the given port", type=int)

class Application(tornado.web.Application):
    
    def __init__(self):
        handlers = [
            (r"/", IndexHandler),
            (r"/problems/", ProblemsHandler),
            
            (r"/admin/", AdminHandler),
        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            debug = True,
        )
        conn = pymongo.Connection("localhost", 27017)
        self.db = conn["Gaea"]
        tornado.web.Application.__init__(self, handlers, **settings)


        
class IndexHandler(tornado.web.RequestHandler):
    
    def get(self):
        self.render("index.html")
        
        
def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
    
if __name__ == "__main__":
    main()