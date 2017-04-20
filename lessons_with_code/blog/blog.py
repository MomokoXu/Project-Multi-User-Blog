import os
import webapp2
import jinja2
import re

from google.appengine.ext import db

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


# 5733953138851840
# Base Handler
class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    # render: sends back to browser what render_str rendered
    def render(self, template, **kw):
        self.response.out.write(render_str(template, **kw))

# Mainpage
""" TODO: JS file for selection different options """
class MainPage(Handler):
    def get(self):
        self.render('index.html')
    def post(self):
        post_id = self.request.get('post_id')
        key = db.Key.from_path('Post', int(post_id), parent = blog_key())
        post = db.get(key)
        # if no such post, display error 404; otherwise render the post page
        if post:
            self.render('permalink.html', post = post)
        else:
            error = "No such post, please enter another post id!"
            self.render('index.html', post_id = post_id, error = error)
# Signup
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
        self.render('signup.html')

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')
        email = self.request.get('email')
        verify = self.request.get('verify')
        have_error = False

        params = dict(username = username, email = email)

        if not valid_username(username):
            params['username_error'] = "That's not a valid username."
            have_error = True

        if not valid_password(password):
            params['password_error'] = "That's not a valid password."
            have_error = True
        elif password != verify:
            params['verify_error'] = "Passwords not match."
            have_error = True

        if not valid_email(email):
            params['email_error'] = "That's not a valid email address."
            have_error = True

        if have_error:
            self.render('signup.html', **params)
        else:
            self.redirect('/welcome?username=' + username)

# 3. Welcome Handler
class Welcome(Handler):
    def get(self):
        username = self.request.get('username')
        if valid_username(username):
            self.render('welcome.html', username = username)
        else:
            self.redirect('/signup')

# Blog pages

# 1. get blog keys from datastore
def blog_key(name = 'default'):
    return db.Key.from_path('blogs', name)

# 2. Post
class Post(db.Model):
    subject = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    created_time = db.DateTimeProperty(auto_now_add = True)
    last_modified_time = db.DateTimeProperty(auto_now = True)

    def render(self):
        self._render_text = self.content.replace('\n', '<br>')
        return render_str('post.html', p = self)

# 3. Blog Front Handeler: Handler for the main blog URL
    # First, look up all of the posts
class BlogFront(Handler):
    def get(self):
        # Looks at all of the posts ordered by creation
        # time and store them in the post object
        posts = Post.all().order('-created_time')
        # generate front page to display most rescent posts
        self.render('front.html', posts = posts)

# 4. Post page Handler: the page for a perticular post
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
    def get(self):
        self.render('newpost.html')

    def post(self):
        subject = self.request.get('subject')
        content = self.request.get('content')

        if subject and content:
            # create new post object and store it into datastore
            p = Post(parent = blog_key(), subject = subject, content = content)
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
                               ('/blog/newpost', NewPost),], debug=True)
