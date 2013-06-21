import tornado.web
import tornado.auth
import tornado.httpserver
import tornado.escape
import pymongo


class BaseHandler(tornado.web.RequestHandler):
    
    def get_current_user(self):
        return self.get_secure_cookie("administrator")

class AdminHomeHandler(BaseHandler):
    
    @tornado.web.authenticated
    def get(self):
        name = self.current_user
        self.render("admin/index.html", name=name)

class AdminLoginHandler(BaseHandler):
    
    def get(self):
        self.render("admin/login.html")

    
    def post(self):
        self.set_secure_cookie("administrator", self.get_argument("name"))
        self.redirect("/admin")


class AdminLogoutHandler(BaseHandler):
    
    def get(self):
        self.clear_cookie("administrator")
        self.write('You are now logged out. Click <a href="/">here</a> to log back in.')


class AddProblemHandler(BaseHandler):
    
    def getNextSequence(self):
        db = self.application.db.ids
        ret = db.find_and_modify(
            {'name': 'problemid'},
            {'$inc': {'id':1}},
            new = True,
            upsert = True,
        )
        return ret['id']
    
    @tornado.web.authenticated 
    def get(self):
        self.render("admin/add_new_problem.html")
        
    @tornado.web.authenticated
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
        self.write("Add new problem %s successful.<br/> <a href=\"/problems\"     >Return to problems Page</a>" % new_problem['title'])
        