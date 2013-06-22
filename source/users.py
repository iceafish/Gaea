import tornado.auth
import tornado.web
import tornado.escape
import pymongo
import base64

class BaseHandler(tornado.web.RequestHandler):
    
    def get_current_user(self):
        return self.get_secure_cookie("user_info")
    

def coding(source):
    return base64.encodestring(source)
    

def uncoding(source):
    return base64.decodestring(source)


class UserLoginHandler(BaseHandler):
    
    def post(self):
        uname = self.get_argument("user_name")
        passwd = self.get_argument("password")
        
        db = self.application.db.users
        confirm = db.find_one({"user_name": uname})
        
        if not confirm:
            self.write("User %s not exist." % uname)
            return 
        
        decode_pw = uncoding(confirm["passwd"])
        
        if passwd != decode_pw:
            self.write("wrong password.")
            return 
        
        self.set_secure_cookie("user_info", uname)
        self.redirect("/")

class UserLogoutHandler(BaseHandler):
    
    def get(self):
        self.clear_cookie("user_info")
        self.redirect("/")

class RegisterUserHandler(BaseHandler):
    
    def get(self):
        return self.render("users/register.html")
    
    def post(self):
        db = self.application.db.users
        uname = self.get_argument("user_name")
        pw = self.get_argument("password")
        exist = db.find({"user_name": uname}).count()
        if exist != 0:
            self.write("user is exist.")
            return
        
        code_pw = coding(pw)
        
        new_user = {
            "user_name": uname,
            "passwd": code_pw,
            "email": self.get_argument("email"),
            "group": "student",
            
            "info": {
                "accept": 0,
                "submit": 0,
            }
        }
        
        db.insert(new_user)
        self.redirect("/")