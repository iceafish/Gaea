import tornado.httpserver
import tornado.web
import time
import json
from jserver import AddRequest

class BaseHandler(tornado.web.RequestHandler):
    
    def get_current_user(self):
        return self.get_secure_cookie("user_info")

class ProblemsHandler(tornado.web.RequestHandler):
    
    def get(self):
        coll = self.application.db.problems
        self.render("problemlist.html", problems=coll.find().sort("_id"))

class ShowProblemHandler(BaseHandler):
    
    def get(self, problem_id):
        coll = self.application.db.problems
        problem = coll.find_one({'_id':int(problem_id)})
        if problem == None:
            self.set_status("404", "Problem not found")
            return 
        
        if self.current_user:
            name = self.current_user
        else:
            name = "None"
        
        self.render("problemInfo.html", problem = problem, curuser = name)
    
class SubmitProblemHandler(BaseHandler):
    
    def getNextSequence(self):
        db = self.application.db.ids
        ret = db.find_and_modify(
            {'name': 'request_id'},
            {'$inc': {'id':1}},
            new = True,
            upsert = True,
        )
        return ret['id']
    
    @tornado.web.authenticated
    def post(self, problem_id):
        new_post = {
            "_id": self.getNextSequence(),
            "problem_id": int(problem_id),
            "language_type": self.get_argument("language"),
            "user_name": self.current_user,
            "submit_date": time.ctime(),
            "result": None
        }

        submit_file = self.request.files["code_file"][0]
        file_type = submit_file['filename'].split('.')[-1]
        if not file_type:
            self.write("file type error")
            return 
        
        file_name = "./judger/SourceCode/%d.%s" % (new_post['_id'],file_type)
        
        fin = open(file_name, 'w')
        fin.write(submit_file['body'])
        fin.close()
        
        new_post['code_file'] = file_name
        
        db_judge_queues = self.application.db.judge_queues
        db_judge_queues.insert(new_post)
        
        db_users = self.application.db.users
        db_users.find_and_modify(
            {'user_name': new_post['user_name']},
            {'$inc': {'info.submit': 1}}
        )
        
        db_problems = self.application.db.problems
        db_problems.find_and_modify(
            {'_id': new_post['problem_id']},
            {'$inc': {'info.total': 1}}
        )

        problem = self.application.db.problems.find_one({'_id': new_post['problem_id']})
        req = {
            '_id': new_post['_id'],
            'problem_id': new_post['problem_id'],
            'language_type': new_post['language_type'],
            'time_limit': problem['time_limit'],
            'memory_limit': problem['memory_limit'],
            'source_file_name': new_post['code_file'].split('/')[-1],
            'data_files': problem['data_files']
        }
        AddRequest(json.dumps(req))

        self.redirect('/status')