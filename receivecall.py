import webapp2
import twilio.twiml

class ReceiveCall(webapp2.RequestHandler):
    def post(self):
        resp = twilio.twiml.Response()
        resp.say("Hello world!")

        self.response.write(str(resp))
