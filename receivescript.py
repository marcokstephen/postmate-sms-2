import webapp2

class ReceiveScript(webapp2.RequestHandler):
    def post(self):
        self.response.write("This is for receiving the transcript")
