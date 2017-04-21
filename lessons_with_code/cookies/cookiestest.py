import os
import webapp2
import jinja2
import re

from google.appengine.ext import db

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

class MainPage(Handler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        # get a cookie called visits:
            # request object will have a cookie object,
            # and get cookie with key = 'visits', the key exist, get the value,
            # if not set it to zero
        visits = self.request.cookies.get('visits', 0)

        #make sure visits is an int
        if visits.isdigit():
            # as visit times increases, increates number of times
            visits = int(visits) + 1
        else:
            visits = 0

        # store the visits time into cookie so next time we refresh the page we
            # will get the times
        # The way we set cookie in App engine is just set the cookie header.
        self.response.headers.add_header('Set-cookie', 'visits=%s' % visits)
        if visits > 1000:
            self.write("You are the best ever!!")
        else:
            self.write("You have been here %s times" % visits) # print visited times

app = webapp2.WSGIApplication([('/', MainPage)], debug=True)