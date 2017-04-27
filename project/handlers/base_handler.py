import webapp2
from models import User
from utility import check_secure_val, make_secure_val, render_str


######### Base Handler #########
class Handler(webapp2.RequestHandler):
    def __init__(self, *a, **kw):
        webapp2.RequestHandler.initialize(self, *a, **kw)
        uid = self.read_cookie('user_id')
        self.user = uid and User.by_id(int(uid))

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    # render_str: take user into account to render page
    def render_str(self,template, **params):
        params['user'] = self.user
        return render_str(template, **params)

    # render: sends back to browser what self.render_str rendered
    def render(self, template, **kw):
        self.response.out.write(self.render_str(template, **kw))

    # set and read cookie
    def set_cookie(self, name, val):
        cookie_val = make_secure_val(val)
        self.response.headers.add_header('Set-cookie',
                                         '%s=%s; Path=/' % (name, cookie_val))
    def read_cookie(self, name):
        cookie_val = self.request.cookies.get(name)
        return cookie_val and check_secure_val(cookie_val)

    # implement login
    def login(self, user):
        self.set_cookie('user_id', str(user.key().id()))

    # implemnet logout
    def logout(self):
        self.response.headers.add_header('Set-cookie', 'user_id=; Path=/')