from base_handler import Handler
from models import User, Post
from utility import valid_username, valid_password, valid_email

######### Signup #########

# Signup Handler
class Signup(Handler):
    def get(self):
        if self.user:
            return self.redirect('/')
        else:
            self.render('signup.html')

    def post(self):
        self.username = self.request.get('username')
        self.password = self.request.get('password')
        self.email = self.request.get('email')
        self.verify = self.request.get('verify')
        have_error = False

        params = dict(username = self.username, email = self.email)

        if not valid_username(self.username):
            params['username_error'] = "That's not a valid username."
            have_error = True

        if not valid_password(self.password):
            params['password_error'] = "That's not a valid password."
            have_error = True
        elif self.password != self.verify:
            params['verify_error'] = "Passwords not match."
            have_error = True

        if not valid_email(self.email):
            params['email_error'] = "That's not a valid email address."
            have_error = True

        if have_error:
            self.render('signup.html', **params)
        else:
            self.done()

    def done(self):
        # check existing user first
        usr = User.by_name(self.username)
        if usr:
            # if already exist, show error message
            error = "User name already exists."
            self.render('signup.html', username_error=error)
        else:
            # if not exist, create new user and store into db
            # then login user and redirect to welcome page
            usr = User.register(self.username, self.password, self.email)
            usr.put()
            self.login(usr)
            return self.redirect('/welcome')

########## Login #########
class Login(Handler):
    def get(self):
        if self.user:
            return self.redirect('/')
        else:
            self.render('login.html')

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')

        usr = User.login(username, password)
        if usr:
            self.login(usr)
            return self.redirect('/welcome')
        else:
            error = "Invalid login, try again"
            self.render('login.html', error=error)

########## Logout #########
class Logout(Handler):
    def get(self):
        self.logout()
        self.render('logout.html')

########## Welcome #########
class Welcome(Handler):
    def get(self):
        if self.user:
            # Looks at all of the posts ordered by creation
            # time and store them in the post object
            posts = Post.all().order('-created_time')
            # generate front page to display most rescent posts
            self.render('welcome.html', username = self.user.name, posts=posts)
        else:
            return self.redirect('/signup')