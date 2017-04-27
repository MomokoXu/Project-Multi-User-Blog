import hmac
import re
import os
import jinja2
import hashlib
import hmac
from google.appengine.ext import db
import random
from string import letters

# Jinjia template engine:render page
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)
def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

# Hash cookie
SECRET = 'momoko'
def hash_str(s):
    return hmac.new(SECRET, s).hexdigest()

def make_secure_val(s):
    return "%s|%s" % (s, hash_str(s))

def check_secure_val(h):
    hstr = h.split('|')[0]
    if h == make_secure_val(hstr):
        return hstr

# Validate signup
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")
def valid_email(email):
    return not email or EMAIL_RE.match(email)


# Hash password
def make_salt(length = 5):
    return ''.join(random.choice(letters) for x in xrange(length))

def make_pw_hash(name, pw, salt = None):
    if not salt:
        salt = make_salt()
    h = hashlib.sha256(name + pw + salt).hexdigest()
    return '%s,%s' % (salt, h)

def valid_pw(name, password, h):
    salt = h.split(',')[0]
    return h == make_pw_hash(name, password, salt)

# Model keys
def users_key(group = 'default'):
    return db.Key.from_path('users', group)


def blog_key(name = 'default'):
    return db.Key.from_path('blogs', name)

def comment_key(name = 'default'):
    return db.Key.from_path('comments', name)


def like_key(name = 'default'):
    return db.Key.from_path('likes', name)