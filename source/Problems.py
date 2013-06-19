import tornado.httpserver
import tornado.web
import pymongo

class ProblemsHandler(tornado.web.RequestHandler):
    
    def get(self):
        coll = self.application.db.problems
        self.render("problemlist.html", problems=coll.find().sort("_id"))

class ShowProblemHandler(tornado.web.RequestHandler):
    
    def get(self, problem_id):
        coll = self.application.db.problems
        problem = coll.find_one({'_id':int(problem_id)})
        if problem == None:
            self.set_status("404", "Problem not found")
            return 
        self.render("problemInfo.html", problem = problem )
    