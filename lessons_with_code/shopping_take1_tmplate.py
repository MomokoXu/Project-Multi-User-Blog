import webapp2


form_html="""
<form>
<h2>Add a Food<h2>
<input type="text" name="food">
%s
<button>Add</button>
</form>
"""

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

class MainPage(Handler):
	def get(self):
		# output is what we are going to return to user
		output = form_html
		# hold what we are going to subtitute into and where hidden inputs go
		output_hidden = ""
		# if there are multi parameters with the same name, get_all will put them into a list
		items = self.request.get_all("food")
		if items:
			output_items = ""
			for item in items:
				output_hidden += hidden_html % item
				output_items += item_html % item

			output_shopping = shopping_list_html % output_items
			output += output_shopping

		output = output % output_hidden

		self.write(output)

'''
# jinja test

class JinjiaTestHandler(Handler):
	def get(self):
		test jinja statement syntax
		n = self.request.get("n")
		if n:
			n = int(n)
		self.render("shopping_list.html", n = n)

		test jinja variable substitution
		self.render("shopping_list.html", animal1=self.request.get("animal1"), animal2=self.request.get("animal2"))


# Fizzbuzz test
class FizzBuzzHandler(Handler):
	def get(self):
		n = self.request.get('n', 0)
		n = n and int(n)
		self.render("fizzbuzz.html", n = n)
'''

app = webapp2.WSGIApplication([('/', MainPage)], debug=True)
