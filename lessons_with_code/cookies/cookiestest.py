import os
import webapp2
import jinja2
import re

from google.appengine.ext import db

import hashlib
import hmac
import random
import string

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)
def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)
class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    # render: sends back to browser what render_str rendered
    def render(self, template, **kw):
        self.response.out.write(render_str(template, **kw))

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

"""Hash Cookie"""
def hash_str_no_secret(s):
    return hashlib.md5(s).hexdigest()

# Implement the hash_str function to use HMAC and our SECRET instead of md5
SECRET = 'imsosecret'
def hash_str(s):
    return hmac.new(SECRET, s).hexdigest()


# Implement the function make_secure_val, which takes a string and returns a
# string of the format:
# s,HASH

def make_secure_val(s):
    return "%s|%s" % (s, hash_str(s))

# Implement the function check_secure_val, which takes a string of the format
# s,HASH
# and returns s if hash_str(s) == HASH, otherwise None

def check_secure_val(h):
    str = h.split('|')[0]
    if h == make_secure_val(str):
        return str

"""password hasing"""
# Implement the function make_salt() that returns a string of 5 random
# letters use python's random module.
# Note: The string package might be useful here.

def make_salt():
    return ''.join(random.choice(string.letters) for x in range(5))
# implement the function make_pw_hash(name, pw) that returns a hashed password
# of the format:
# HASH(name + pw + salt),salt
# use sha256

def make_pw_hash_old(name, pw):
    salt = make_salt()
    print salt
    return "%s,%s" % (hashlib.sha256(name + pw + salt).hexdigest(), salt)

# Implement the function valid_pw() that returns True if a user's password
# matches its hash. You will need to modify make_pw_hash.

def make_pw_hash(name, pw, salt=None):
    if not salt:
        salt = make_salt()
    h = hashlib.sha256(name + pw + salt).hexdigest()
    return '%s,%s' % (h, salt)

def valid_pw(name, pw, h):
    salt = h.split(',')[1]
    return h == make_pw_hash(name, pw, salt)


class MainPage(Handler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        # get a cookie called visits:
            # request object will have a cookie object,
            # and get cookie with key = 'visits', the key exist, get the value,
            # if not set it to zero
        """
        visits = self.request.cookies.get('visits', 0)
        #make sure visits is an int
        if visits.isdigit():
            # as visit times increases, increates number of times
            visits = int(visits) + 1
        else:
            visits = 0
        """
        """With hashed cookie"""
        visits = 0
        visits_cookie_str = self.request.cookies.get('visits')
        if visits_cookie_str:
            cookie_val = check_secure_val(visits_cookie_str)
            if cookie_val:
                visits = int(cookie_val)
        visits += 1
        new_cookie_val = make_secure_val(str(visits))
        # store the visits time into cookie so next time we refresh the page we
            # will get the times
        # The way we set cookie in App engine is just set the cookie header.
        self.response.headers.add_header('Set-cookie', 'visits=%s' % new_cookie_val)
        if visits > 1000:
            self.write("You are the best ever!!")
        else:
            self.write("You have been here %s times" % visits) # print visited times

app = webapp2.WSGIApplication([('/', MainPage)], debug=True)