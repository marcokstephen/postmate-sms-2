import webapp2

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.write("Hello world! This is the main page of our app.")
