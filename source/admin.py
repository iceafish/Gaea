import tornado.web
import tornado.httpserver
import pymongo

class AdminHomeHandler(tornado.web.RequestHandler):
    
    def get(self):
        self.render("admin/index.html")


class AddProblemHandler(tornado.web.RequestHandler):
    
    def getNextSequence(self):
        db = self.application.db.ids
        ret = db.find_and_modify(
            {'name': 'problemid'},
            {'$inc': {'id':1}},
            new = True,
            upsert = True,
        )
        return ret['id']
        
    def get(self):
        self.render("admin/add_new_problem.html")
    
    def post(self):
        new_problem = {
            "_id" : self.getNextSequence(),
            "title" : self.get_argument("title"),
            
            "time_limit" : self.get_argument("time_limit"),
            "memory_limit" : self.get_argument("memory_limit"),
            "use_able" : self.get_argument("use_able"),
            
            "description" : self.get_argument("description"),
            "input" : self.get_argument("input"),
            "output" : self.get_argument("output"),
            "sample_input" : self.get_argument("sample_input"),
            "sample_output" : self.get_argument("sample_output"),
            "hint" : self.get_argument("hint"),
            "source" : self.get_argument("source"),
            
            "total" : 0,
            "AC" : 0,
            "WA" : 0,
            "TLE" : 0,
            "MLE" : 0,
            "PE" : 0,
            "ratio" : 0
        }
        print new_problem
        db = self.application.db.problems
        db.insert( new_problem )
        self.write("Add new problem %s successful.<br/> <a href=\"/problems/\"     >Return to problems Page</a>" % new_problem['title'])
        