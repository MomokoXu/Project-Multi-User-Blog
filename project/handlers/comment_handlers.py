from base_handler import Handler
from models import User, Post, Comment
from google.appengine.ext import db
from utility import blog_key, comment_key
import time

######## Comment Handlers ########
# New Comment Handler
class NewComment(Handler):
    def get(self, post_id):
        if not self.user:
            error = "Login please!"
            return self.render('/index.html', login_error = error)
        key = db.Key.from_path('Post', int(post_id), parent = blog_key())
        post = db.get(key)
        if not post:
            return self.redirect('/blog')
        self.render('newcomment.html', post_id = post_id)

    def post(self, post_id):
        if not self.user:
            error = "Login please!"
            return self.render('/index.html', login_error = error)
        key = db.Key.from_path('Post', int(post_id), parent = blog_key())
        post = db.get(key)
        if not post:
            return self.redirect('/blog')

        comment = self.request.get('comment')

        if comment:
            c = Comment(parent = comment_key(),
                              content = comment,
                              post = post,
                              user = self.user)
            c.put()
            time.sleep(0.1)
            return self.redirect('/blog/%s' % post_id)
        else:
            error = 'Please enter your comment!'
            self.render('newcomment.html', comment = comment,
                                           error = error,
                                           post_id = post_id)

# Edit Comment Handler
class EditComment(Handler):
    def get(self, post_id, comment_id):
        if not self.user:
            error = "Login please!"
            return self.render('/index.html', login_error = error)
        pkey = db.Key.from_path('Post', int(post_id), parent = blog_key())
        post = db.get(pkey)
        if not post:
            return redirect('/blog/%s' % post_id)

        ckey = db.Key.from_path('Comment', int(comment_id), parent = comment_key())
        comment = db.get(ckey)
        if comment and self.user.key().id() == comment.user.key().id():
            self.render('editcomment.html', post_id = post_id, comment = comment.content)
        else:
            return self.redirect('/blog/%s' % post_id)

    def post(self, post_id, comment_id):
        if not self.user:
            error = "Login please!"
            return self.render('/index.html', login_error = error)
        pkey = db.Key.from_path('Post', int(post_id), parent = blog_key())
        post = db.get(pkey)
        if not post:
            return redirect('/blog/%s' % post_id)

        ckey = db.Key.from_path('Comment', int(comment_id), parent = comment_key())
        comment = db.get(ckey)
        if not comment or self.user.key().id() != comment.user.key().id():
            return self.redirect('/blog/%s' % post_id)

        content = self.request.get('comment')
        if content:
            comment.content = content
            comment.put()
            time.sleep(0.1)
            return self.redirect('/blog/%s' % post_id)
        else:
            error = 'Please enter your comment!'
            self.render('editcomment.html', comment = content,
                                           error = error,
                                           post_id = post_id)


# Delete Comment Handeler
class DeleteComment(Handler):
    def get(self, post_id, comment_id):
        if not self.user:
            error = "Login please!"
            return self.render('/index.html', login_error = error)
        pkey = db.Key.from_path('Post', int(post_id), parent = blog_key())
        post = db.get(pkey)
        if not post:
            return redirect('/blog/%s' % post_id)

        ckey = db.Key.from_path('Comment', int(comment_id), parent = comment_key())
        comment = db.get(ckey)
        if not comment:
            return self.redirect('/blog/%s' % post_id)
        if self.user.key().id() != comment.user.key().id():
            return self.redirect('/blog/%s' % post_id)
        comment.delete()
        time.sleep(0.1)
        return self.redirect('/blog/%s' % post_id)