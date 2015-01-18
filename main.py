import webapp2
from mainpage import MainPage
from receivetext import ReceiveText
from receivecall import ReceiveCall

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/receivetext', ReceiveText),
    ('/receivecall', ReceiveCall(
], debug=True)
