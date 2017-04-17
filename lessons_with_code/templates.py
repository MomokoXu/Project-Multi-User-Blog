import os
import webapp2
import jinja2

# os.path.join: concatenates two file names:
	# os.path.dirname(__file__) directory of my current file is in
	# 'templates'
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
# jinja_env: it means we render templates, jinja will look for those tmeplates in template_dir
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir))


# value will be substituted with different item
hidden_html="""
<input type="hidden" name="food" value="%s">
"""

item_html="<li>%s</li>"

# ul: unorder list
shopping_list_html="""
<br>
<br>
<h2>Shopping List</h2>
<ul>
%s
</ul>
"""

class Handler(webapp2.RequestHandler):
	def write(self, *a, **kw):
		self.response.out.write(*a, **kw)

	# render_str: takes a file name: template, and abrunch of parameters: **params
		# t: use jinja environment created earlier, then call get_template with
			# the file name. This basically causes jinja to load that file and create
			# a jinja template, and store it into t
		# call t.render passing the parameters that were passed into this function.
			# which is anctully string
	def render_str(self, template, **params):
		t = jinja_env.get_template(template)
		return t.render(params)

	# render: sends back to browser what render_str rendered
	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))


class MainPage(Handler):
	def get(self):
		# test jinja statement syntax
		'''
		n = self.request.get("n")
		if n:
			n = int(n)
		self.render("shopping_list.html", n = n)
		'''
		# test jinja variable substitution
		# self.render("shopping_list.html", animal1=self.request.get("animal1"), animal2=self.request.get("animal2"))
		'''
		# output is what we are going to return to user
		output = form_html
		# hold what we are going to subtitute into and where hidden inputs go
		output_hidden = ""
		# if there are multi parameters with the same name, get_all will put them into a list
		items = self.request.get_all("food")
		if items:
			output_items = ""
			for item in items:
				output_hidden += hidden_html % item_html
				output_items += item_html % item

			output_shopping = shopping_list_html % output_items
			output += output_shopping

		output = output % output_hidden

		self.write(output)
		'''
		# shoppling list Take 2
		items = self.request.get_all("food")
		self.render("shopping_list.html", items=items)
'''
# Fizzbuzz test
class FizzBuzzHandler(Handler):
	def get(self):
		n = self.request.get('n', 0)
		n = n and int(n)
		self.render("fizzbuzz.html", n = n)
'''

app = webapp2.WSGIApplication([('/', MainPage)], debug=True)
