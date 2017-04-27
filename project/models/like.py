from google.appengine.ext import db
from user import User
from post import Post

class Like(db.Model):
    user = db.ReferenceProperty(User, required=True, collection_name='user_likes')
    post = db.ReferenceProperty(Post, required=True, collection_name='post_likes')