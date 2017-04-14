import webapp2

'''
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
		<option value="1">The numebr one</option>
		<option value="2">Two</option>
		<option value="3">Three</option>
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
'''

#What's your brithday
form="""
<form method="post">
	What is your birthday?
	<br>
	<label> Month
		<input name="month">
	</label>
	<label> Day
	<input name="day">
	</label>
	<label> Year
	<input name="year">
	</label>
	<input type="submit">
</form>
"""

# Valid month
months = ['January',
          'February',
          'March',
          'April',
          'May',
          'June',
          'July',
          'August',
          'September',
          'October',
          'November',
          'December']

# as long as the first 3 letters match then return
month_abbvs = dict((m[:3].lower(), m) for m in months)

def valid_month(month):
	if month:
		short_month = month[:3].lower()
		return month_abbvs.get(short_month)

# Valid day
def valid_day(day):
	if day and day.isdigit() and int(day) in range(1, 32):
		return int(day)

# Valid year
def valid_year(year):
	if year and year.isdigit() and int(year) in range(1900, 2020):
		return int(year)

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.write(form)
    def post(self):
    	self.response.out.write("Thanks! That's a totally valid day!")

app = webapp2.WSGIApplication([('/', MainPage)], debug=True)
