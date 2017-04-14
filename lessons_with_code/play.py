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
	<input type="checkbox" name="r">
	<input type="checkbox" name="s">
	<br>
	<input type="submit">
</form>
"""
#radio buttons
form5="""
<form>
	<input type="radio" name="q">
	<input type="radio" name="r">
	<input type="radio" name="s">
	<br>
	<input type="submit">
</form>
"""

form6="""
<form>
	<input type="radio" name="q" value="one">
	<input type="radio" name="q" value="two">
	<input type="radio" name="q" value="three">
	<br>
	<input type="submit">
</form>
"""
#label element
form7="""
<form>
	<label>
		One
		<input type="radio" name="q" value="one">
	</label>
	<label>
		Two
		<input type="radio" name="q" value="two">
	</label>
	<label>
		Three
		<input type="radio" name="q" value="three">
	</label>
	<br>
	<input type="submit">
</form>
"""
#dropdown
form8="""
<form>
	<select name="q">
		<option>One</option>
		<option>Two</option>
		<option>Three</option>
	</select>
	<br>
	<input type="submit">
</form>
"""

class MainPage(webapp2.RequestHandler):
    def get(self):
        #self.response.headers['Content-Type'] = 'text/plain'
        self.response.write(form8)

class TestHandler(webapp2.RequestHandler):
	def post(self):
		#q = self.request.get("q")
		#self.response.out.write(q)
		self.response.headers['Content-Type'] = 'text/plain'
		self.response.write(self.request)

app = webapp2.WSGIApplication([
    ('/', MainPage), ('/testform', TestHandler)
], debug=True)
