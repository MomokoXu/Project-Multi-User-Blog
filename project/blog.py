import os
import webapp2
import jinja2
import re
import hmac
from google.appengine.ext import db

from user import User

# os.path.join: concatenates two file names:
    # os.path.dirname(__file__) directory of my current file is in
    # 'templates'
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
# jinja_env: it means we render templates, jinja will look for those tmeplates
# in template_dir
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)


def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

########## Cookie Hasing #########
SECRET = 'momoko'
def hash_str(s):
    return hmac.new(SECRET, s).hexdigest()

def make_secure_val(s):
    return "%s|%s" % (s, hash_str(s))

def check_secure_val(h):
    hstr = h.split('|')[0]
    if h == make_secure_val(hstr):
        return hstr

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

########## Mainpage #########
class MainPage(Handler):
    def get(self):
        self.render('index.html')
    def post(self):
        post_id = self.request.get('post_id')
        try:
            key = db.Key.from_path('Post', int(post_id), parent = blog_key())
            post = db.get(key)
            # if no such post, display error 404; otherwise render the post page
            if post:
                self.render('permalink.html', post = post)
            else:
                error = "No such post, please enter another post id!"
                self.render('index.html', post_id = post_id, error = error)
        except(ValueError):
                error = "Invalid post id, try again!"
                self.render('index.html', error = error)


######### Signup #########
# 1. check regular expression matching for username, password and email
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")
def valid_email(email):
    return not email or EMAIL_RE.match(email)

# 2. Signup Handler
class Signup(Handler):
    def get(self):
        if self.user:
            signup_error="You already have a account and you are logged in!"
            self.render('/index.html', signup_error=signup_error)
        else:
            self.render('signup.html')

    def post(self):
        self.username = self.request.get('username')
        self.password = self.request.get('password')
        self.email = self.request.get('email')
        self.verify = self.request.get('verify')
        have_error = False

        params = dict(username = self.username, email = self.email)

        if not valid_username(self.username):
            params['username_error'] = "That's not a valid username."
            have_error = True

        if not valid_password(self.password):
            params['password_error'] = "That's not a valid password."
            have_error = True
        elif self.password != self.verify:
            params['verify_error'] = "Passwords not match."
            have_error = True

        if not valid_email(self.email):
            params['email_error'] = "That's not a valid email address."
            have_error = True

        if have_error:
            self.render('signup.html', **params)
        else:
            self.done()

    def done(self):
        # check existing user first
        usr = User.by_name(self.username)
        if usr:
            # if already exist, show error message
            error = "User name already exists."
            self.render('signup.html', username_error=error)
        else:
            # if not exist, create new user and store into db
            # then login user and redirect to blog page
            usr = User.register(self.username, self.password, self.email)
            usr.put()
            self.login(usr)
            self.redirect('/welcome')

########## Login #########
class Login(Handler):
    def get(self):
        if self.user:
            login_error="You are already logged in!"
            self.render('/index.html', login_error=login_error)
        else:
            self.render('login.html')

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')

        usr = User.login(username, password)
        if usr:
            self.login(usr)
            msg = "Welcome back"
            self.redirect('/welcome')
        else:
            error = "Invalid login, try again"
            self.render('login.html', error=error)

########## Logout #########
class Logout(Handler):
    def get(self):
        self.logout()
        self.render('logout.html')

########## Welcome #########
class Welcome(Handler):
    def get(self):
        if self.user:
            # Looks at all of the posts ordered by creation
            # time and store them in the post object
            posts = Post.all().order('-created_time')
            # generate front page to display most rescent posts
            self.render('welcome.html', username = self.user.name, posts=posts)
        else:
            self.redirect('/signup')

######### Blog pages #########
# 1. get blog keys from datastore
def blog_key(name = 'default'):
    return db.Key.from_path('blogs', name)

# 2. Post
class Post(db.Model):
    subject = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    author = db.StringProperty(required = True)
    created_time = db.DateTimeProperty(auto_now_add = True)
    last_modified_time = db.DateTimeProperty(auto_now = True)

    def render(self):
        self._render_text = self.content.replace('\n', '<br>')
        return render_str('post.html', p = self)

# 3. Blog Front Handeler: Handler for the main blog URL
class BlogFront(Handler):
    def get(self):
        # Looks at all of the posts ordered by creation
        # time and store them in the post object
        posts = Post.all().order('-created_time')
        # generate front page to display most rescent posts
        self.render('front.html', posts = posts)

# 4. Post page Handler: page for a perticular post
class PostPage(Handler):
    def get(self, post_id):
        # make a key based on the post_id in Post objects
        # and then get the coressponding post by key from datastore
        key = db.Key.from_path('Post', int(post_id), parent = blog_key())
        post = db.get(key)
        # if no such post, display error 404; otherwise render the post page
        if not post:
            self.error(404)
            return
        self.render('permalink.html', post = post)

# 5. New Post Handler: the page for posting new post
class NewPost(Handler):
    # check user exsit or not first
    def get(self):
        if self.user:
            self.render('newpost.html')
        else:
            error = "Login first please!"
            self.render('/index.html', newpost_error = error)

    def post(self):
        if not self.user:
            self.redirect('/blog')

        subject = self.request.get('subject')
        content = self.request.get('content')
        author = self.user.name

        if subject and content:
            # create new post object and store it into datastore
            p = Post(parent = blog_key(),
                     subject = subject,
                     content = content,
                     author = author)
            p.put()
            self.redirect('/blog/%s' % str(p.key().id()))
        else:
            error = 'Please enter both subject and content!'
            self.render('newpost.html', subject= subject, content = content,
                                        error = error)

app = webapp2.WSGIApplication([('/', MainPage),
                               ('/signup', Signup),
                               ('/welcome', Welcome),
                               ('/blog', BlogFront),
                               ('/blog/([0-9]+)', PostPage),
                               ('/blog/newpost', NewPost),
                               ('/login', Login),
                               ('/logout', Logout)], debug=True)
