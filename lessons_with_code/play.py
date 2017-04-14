import webapp2

#action
form="""
<form action="https://www.google.com/search">
	<input name="q">
	<input type="submit">
</form>
"""
#method
form2="""
<form method="post" action="/testform">
	<input name="q">
	<input type="submit">
</form>
"""
#type
form3="""
<form>
	<input type="password" name="q">
	<input type="submit">
</form>
"""
#checkbox
form4="""
<form>
	<input type="checkbox" name="q">
	<input type="submit">
</form>
"""

class MainPage(webapp2.RequestHandler):
    def get(self):
        #self.response.headers['Content-Type'] = 'text/plain'
        self.response.write(form4)

class TestHandler(webapp2.RequestHandler):
	def post(self):
		#q = self.request.get("q")
		#self.response.out.write(q)
		self.response.headers['Content-Type'] = 'text/plain'
		self.response.write(self.request)

app = webapp2.WSGIApplication([
    ('/', MainPage), ('/testform', TestHandler)
], debug=True)
