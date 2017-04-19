import os
import webapp2
import jinja2

# os.path.join: concatenates two file names:
	# os.path.dirname(__file__) directory of my current file is in
	# 'templates'
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
# jinja_env: it means we render templates, jinja will look for those tmeplates in template_dir
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

class Handler(webapp2.RequestHandler):
	def write(self, *a, **kw):
		self.response.out.write(*a, **kw)

	def render_str(self, template, **params):
		t = jinja_env.get_template(template)
		return t.render(params)

	# render: sends back to browser what render_str rendered
	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))


class MainPage(Handler):
	def get(self):
		# shoppling list Take 2
		items = self.request.get_all("food")
		self.render("shopping_list.html", items=items)

class FizzBuzzHandler(Handler):
	def get(self):
		n = self.request.get('n', 0)
		n = n and int(n)
		self.render("fizzbuzz.html", n = n)


app = webapp2.WSGIApplication([('/', MainPage), ('/fizzbuzz', FizzBuzzHandler)], debug=True)

