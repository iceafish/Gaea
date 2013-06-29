import tornado.web
import tornado.auth
import tornado.httpserver
import tornado.escape
import pymongo
import os

class BaseHandler(tornado.web.RequestHandler):
    
    def get_current_user(self):
        return self.get_secure_cookie("user_info")

class AdminHomeHandler(BaseHandler):
    
    @tornado.web.authenticated
    def get(self):
        name = self.current_user

        problems = self.application.db.problems.find()

        self.render("admin/index.html", name=name, problems=problems)

class AdminLoginHandler(BaseHandler):
    
    def get(self):
        self.render("admin/login.html")

    
    def post(self):
        self.set_secure_cookie("user_info", self.get_argument("name"))
        self.redirect("/admin")

class AdminLogoutHandler(BaseHandler):
    
    def get(self):
        self.clear_cookie("user_info")
        self.write('You are now logged out. Click <a href="/">here</a> to log back in.')

class AddDataFileIndexHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        problems = self.application.db.problems.find()
        self.render('admin/add_data_index.html', problems=problems)

class AddDataFileHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self, problem_id):

        problem = self.application.db.problems.find_one({'_id':int(problem_id)})
        if not problem:
            self.write('problem not exist.')
            return
        self.render("admin/add_data.html")

    @tornado.web.authenticated
    def post(self, problem_id):

        problem = self.application.db.problems.find_one({'_id':int(problem_id)})
        if not problem:
            self.write('problem not exist.')
            return

        data_dir = './judger/DataFile/' + problem_id + '/'

        input_file = self.request.files['input_file'][0]
        output_file = self.request.files['output_file'][0]
        input_name,input_type = input_file['filename'].split('.')
        output_name,output_type = output_file['filename'].split('.')

        if input_name!=output_name or input_type!='in' or output_type!='out':
            self.write('data file type error.')
            return

        data_file = [
            {'name':data_dir + input_file['filename'], 'body': input_file['body']},
            {'name':data_dir + output_file['filename'], 'body': output_file['body']}
        ]

        for item in data_file:
            fin = open(item['name'], 'w')
            fin.write(item['body'])
            fin.close()

        problem['data_files'].append(input_file['filename'].split('.')[0])

        self.application.db.problems.save(problem)

        self.redirect('/admin/add/data')


class AddProblemHandler(BaseHandler):
    
    def getNextSequence(self):
        db = self.application.db.ids
        ret = db.find_and_modify(
            {'name': 'problem_id'},
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
            "_id": self.getNextSequence(),
            "title": self.get_argument("title"),
            
            "time_limit": int(self.get_argument("time_limit")),
            "memory_limit": int(self.get_argument("memory_limit")),
            "use_able": self.get_argument("use_able"),
            
            "description" : self.get_argument("description"),
            "input": self.get_argument("input"),
            "output": self.get_argument("output"),
            "sample_input": self.get_argument("sample_input"),
            "sample_output": self.get_argument("sample_output"),
            "hint": self.get_argument("hint"),
            "source": self.get_argument("source"),

            "data_files": [],

            "info": {
                'total' : 0,
                'Yes': 0,
                'Presentation Error': 0,
                'Time Limit Exceeded': 0,
                'Memory Limit Exceeded': 0,
                'Wrong Answer': 0,
                'Runtime Error': 0,
                'Output Limit Exceeded': 0,
                'Compile Error': 0,
                'System Error': 0
            }
        }
        print new_problem
        db = self.application.db.problems
        db.insert( new_problem )

        data_path = './judger/DataFile/'+str(new_problem['_id'])
        if not os.path.exists(data_path):
            os.makedirs(data_path)

        self.write("Add new problem %s successful.<br/> <a href=\"/problems\"     >Return to problems Page</a>" % new_problem['title'])