from base_handler import Handler
from models import User, Post, Like
from google.appengine.ext import db
from utility import blog_key, like_key
import time

######### Like Handlers #########
class LikeBTN(Handler):
    def post(self, post_id):
        if not self.user:
            error = "Login please!"
            return self.render('/index.html', login_error = error)

        pkey = db.Key.from_path('Post', int(post_id), parent = blog_key())
        post = db.get(pkey)
        if not post:
            return redirect('/blog/%s' % post_id)

        if self.user.key().id() == post.user.key().id():
            return self.redirect('/blog/%s' % post_id)

        like_btn = self.request.get('like_btn')
        like = self.user.user_likes.filter('post =', post).get()
        if like_btn == "like" and not like:
            like = Like(user = self.user, post = post, parent=like_key())
            like.put()
        elif like_btn == "unlike" and like:
            like.delete()
        time.sleep(0.1)
        return self.redirect('/blog/%s' % post_id)