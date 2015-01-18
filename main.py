import webapp2
from mainpage import MainPage
from receivetext import ReceiveText
from receivecall import ReceiveCall
from receivescript import ReceiveScript

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/receivetext', ReceiveText),
    ('/receivecall', ReceiveCall),
    ('/receivescript', ReceiveScript)
], debug=True)
