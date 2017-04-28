from base_handler import Handler
from models import User, Post
from google.appengine.ext import db
from utility import blog_key
import time
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
        comments = post.post_comments.order('-last_modified_time')
        liked = self.user and self.user.user_likes.filter('post =', post).count() > 0
        like_num = post.post_likes.count()
        self.render('permalink.html', post = post, user = self.user,
                                      comments = comments, liked = liked,
                                      like_num = like_num)

# New Post Handler: the page for posting new post
class NewPost(Handler):
    # check user exsit or not first
    def get(self):
        if self.user:
            self.render('newpost.html')
        else:
            error = "Log in first please!"
            return self.render('/index.html', newpost_error = error)

    def post(self):
        if not self.user:
            error = "Log in first please!"
            return self.render('/index.html', login_error = error)

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
        if not self.user:
            error = "Login please!"
            return self.render('/index.html', login_error = error)
        key = db.Key.from_path('Post', int(post_id), parent = blog_key())
        post = db.get(key)
        if not post:
            return self.redirect('/blog')
        if self.user.key().id() != post.user.key().id():
            return self.redirect('/blog/%s' % post_id)
        self.render('editpost.html', subject = post.subject,
                    content = post.content, post_id = post_id)

    def post(self, post_id):
        if not self.user:
            error = "Login please!"
            self.render('/index.html', login_error = error)
        key = db.Key.from_path('Post', int(post_id), parent = blog_key())
        post = db.get(key)
        if not post:
            return self.redirect('/blog')
        if self.user.key().id() != post.user.key().id():
            return self.redirect('/blog/%s' % post_id)

        subject = self.request.get('subject')
        content = self.request.get('content')
        if subject and content:
            # change current post object and store it into datastore
            post.subject = subject
            post.content = content
            post.put()
            return self.redirect('/blog/%s' % post_id)
        else:
            error = 'Please enter both subject and content!'
            self.render('editpost.html', subject = subject, content = content,
                                         post_id = post_id, error = error)
# Delete Post Handler
class DeletePost(Handler):
    def get(self, post_id):
        if not self.user:
            error = "Login please!"
            self.render('/index.html', login_error = error)
        key = db.Key.from_path('Post', int(post_id), parent = blog_key())
        post = db.get(key)
        if not post:
            return self.redirect('/blog')
        if self.user.key().id() != post.user.key().id():
            return self.redirect('/blog/%s' % post_id)
        post.delete()
        time.sleep(0.1)
        return self.redirect('/blog')