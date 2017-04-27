from google.appengine.ext import db
from utility import render_str, comment_key
from user import User
from post import Post

class Comment(db.Model):
    user = db.ReferenceProperty(User, required=True, collection_name='user_comments')
    post = db.ReferenceProperty(Post, required=True, collection_name='post_comments')
    content = db.TextProperty(required = True)
    created_time = db.DateTimeProperty(auto_now_add = True)
    last_modified_time = db.DateTimeProperty(auto_now = True)

    def render(self, post, user):
        self._render_text = self.content.replace('\n', '<br>')
        return render_str('comment.html', comment = self,
                                          post = post,
                                          user = user)

    @classmethod
    def by_id(cls, cid):
        return Comment.get_by_id(cid, parent = comment_key())