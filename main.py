import webapp2
from mainpage import MainPage
from receivetext import ReceiveText

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/receivetext', ReceiveText)
], debug=True)
