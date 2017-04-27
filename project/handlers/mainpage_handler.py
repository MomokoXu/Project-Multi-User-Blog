from base_handler import Handler

########## Mainpage #########
class MainPage(Handler):
    def get(self):
        self.render('index.html')
    def post(self):
        post_id = self.request.get('post_id')
        try:
            key = db.Key.from_path('Post', int(post_id), parent = blog_key())
            post = db.get(key)
            # if no such post, display error 404; otherwise render the post page
            if post:
                self.render('permalink.html', post = post)
            else:
                error = "No such post, please enter another post id!"
                self.render('index.html', post_id = post_id, error = error)
        except(ValueError):
                error = "Invalid post id, try again!"
                self.render('index.html', error = error)