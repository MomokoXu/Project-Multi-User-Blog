from google.appengine.ext import db
from utility import render_str
from user import User
# Post model
class Post(db.Model):
    subject = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    user = db.ReferenceProperty(User, required=True, collection_name='user_posts')
    created_time = db.DateTimeProperty(auto_now_add = True)
    last_modified_time = db.DateTimeProperty(auto_now = True)

    def render(self):
        self._render_text = self.content.replace('\n', '<br>')
        return render_str('post.html', p = self)