import tornado.httpserver
import tornado.web
import pymongo

class ProblemsHandler(tornado.web.RequestHandler):
    
    def get(self):
        coll = self.application.db.problems
        self.render("problemlist.html", problems=coll.find().sort("_id"))
