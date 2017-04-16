import webapp2

"""
    What's your birthday example
"""
form="""
<form method="post">
    What is your birthday?
    <br>
    <label>Month<input name="month" value="%(month)s"></label>
    <label>Day<input name="day" value="%(day)s"></label>
    <label>Year<input name="year" value="%(year)s"></label>
    <div style="color: red">%(error)s</div>
    <br>
    <br>
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

# as long as the first 3 letters match then returns
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
    if year and year.isdigit() and int(year) in range(1900, 2021):
        return int(year)

# handle escaping
def escape_html(s):
    for (i, o) in (('&', '&amp;'), ('>', '&gt;'), ('<', '&lt;'), ('"', '&quot;')):
        s = s.replace(i, o)
    return s

class MainPage(webapp2.RequestHandler):
    def write_form(self, error="", month="", day="", year=""):
        escape_month = escape_html(month)
        escape_day = escape_html(day)
        escape_year = escape_html(year)
        self.response.out.write(form % {"error": error,
                                        "month": escape_month,
                                        "day": escape_day,
                                        "year": escape_year})

    def get(self):
        #self.response.out.write(form)
        self.write_form()

    def post(self):
        user_month = self.request.get('month')
        user_day = self.request.get('day')
        user_year = self.request.get('year')

        month = valid_month(user_month)
        day = valid_day(user_day)
        year = valid_year(user_year)

        # if not all 3 of these aren't true, rerender our form again
        if not (month and day and year):
            #self.response.out.write(form)
            self.write_form("That does not look valid for me, friend.", user_month, user_day, user_year)
        else:
            self.response.out.write("Thanks! That's a totally valid day!")

app = webapp2.WSGIApplication([('/', MainPage)], debug=True)
