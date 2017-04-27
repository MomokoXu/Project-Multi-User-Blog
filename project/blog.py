import os
import webapp2
import jinja2
import time
from google.appengine.ext import db
from user import User
from post import Post
from comment import Comment
from utility import render_str
from utility import check_secure_val, make_secure_val
from utility import valid_username, valid_password, valid_email
from utility import blog_key, comment_key


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

# Signup Handler
class Signup(Handler):
    def get(self):
        if self.user:
            return self.redirect('/')
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
            # then login user and redirect to welcome page
            usr = User.register(self.username, self.password, self.email)
            usr.put()
            self.login(usr)
            return self.redirect('/welcome')

########## Login #########
class Login(Handler):
    def get(self):
        if self.user:
            return self.redirect('/')
        else:
            self.render('login.html')

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')

        usr = User.login(username, password)
        if usr:
            self.login(usr)
            return self.redirect('/welcome')
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
            return self.redirect('/signup')


######### Blog pages #########
# Blog Front Handeler: Handler for the main blog URL
class BlogFront(Handler):
    def get(self):
        # Looks at all of the posts ordered by creation
        # time and store them in the post object
        posts = Post.all().order('-created_time')
        # generate front page to display most rescent posts
        self.render('front.html', posts = posts)

# Post page Handler: page for a perticular post
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
        comments = post.post_comments.order('-created_time')
        self.render('permalink.html', post=post, user=self.user, comments=comments)

# New Post Handler: the page for posting new post
class NewPost(Handler):
    # check user exsit or not first
    def get(self):
        if self.user:
            self.render('newpost.html')
        else:
            error = "Log in first please!"
            self.render('/index.html', newpost_error = error)

    def post(self):
        if not self.user:
            return self.redirect('/blog')

        subject = self.request.get('subject')
        content = self.request.get('content')

        if subject and content:
            # create new post object and store it into datastore
            p = Post(parent = blog_key(),
                     subject = subject,
                     content = content,
                     user = self.user)
            p.put()
            return self.redirect('/blog/%s' % str(p.key().id()))
        else:
            error = 'Please enter both subject and content!'
            self.render('newpost.html', subject = subject, content = content,
                                        error = error)
# Edit Post Handler
class EditPost(Handler):
    def get(self, post_id):
        if self.user:
            key = db.Key.from_path('Post', int(post_id), parent = blog_key())
            post = db.get(key)
            self.render('editpost.html', subject=post.subject,
                        content=post.content, post_id=post_id)
        else:
            error = "Login first please!"
            self.render('/permalink.html', edit_error = error)

    def post(self, post_id):
        if not self.user:
            return self.redirect('/blog')

        subject = self.request.get('subject')
        content = self.request.get('content')
        # get post
        key = db.Key.from_path('Post', int(post_id), parent = blog_key())
        post = db.get(key)
        if subject and content:
            # change current post object and store it into datastore
            post.subject = subject
            post.content = content
            post.put()
            return self.redirect('/blog/%s' % str(post_id))
        else:
            error = 'Please enter both subject and content!'
            self.render('editpost.html', subject = subject, content = content,
                                         post_id = post_id, error = error)
# Delete Post Handler
class DeletePost(Handler):
    def get(self, post_id):
        key = db.Key.from_path('Post', int(post_id), parent = blog_key())
        post = db.get(key)
        post.delete()
        time.sleep(0.1)
        return self.redirect('/blog')


######## Comment Handlers ########
# New Comment Handler
class NewComment(Handler):
    def get(self, post_id):
        key = db.Key.from_path('Post', int(post_id), parent = blog_key())
        post = db.get(key)
        if self.user and post:
            self.render('newcomment.html', post_id = post_id)

    def post(self, post_id):
        key = db.Key.from_path('Post', int(post_id), parent = blog_key())
        post = db.get(key)
        if not self.user or not post:
            return self.redirect('/blog')

        comment = self.request.get('comment')

        if comment:
            c = Comment(parent = comment_key(),
                              content = comment,
                              post = post,
                              user = self.user)
            c.put()
            time.sleep(0.2)
            return self.redirect('/blog/%s' % post_id)
        else:
            error = 'Please enter your comment!'
            self.render('newcomment.html', comment = comment,
                                           error = error,
                                           post_id = post_id)

# Edit Comment Handler

# Delete Comment Handeler

app = webapp2.WSGIApplication([('/', MainPage),
                               ('/signup', Signup),
                               ('/welcome', Welcome),
                               ('/blog', BlogFront),
                               ('/blog/([0-9]+)', PostPage),
                               ('/blog/newpost', NewPost),
                               ('/login', Login),
                               ('/logout', Logout),
                               ('/blog/([0-9]+)/edit', EditPost),
                               ('/blog/([0-9]+)/delete', DeletePost),
                               ('/blog/([0-9]+)/comment/newcomment', NewComment)], debug=True)
