import webapp2
from mainpage import MainPage
from receivetext import ReceiveText
from receivecall import *
from receivescript import ReceiveScript

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/receivetext', ReceiveText),
    ('/receivecall', ReceiveCall),
    ('/receivescript', ReceiveScript),
    ('/handle-recording0', ReceiveCall1),
    ('/handle-recording1', ReceiveCall2),
    ('/handle-recording2', ReceiveCall3),
    ('/transcribe0',Transcribe0),
    ('/transcribe1',Transcribe1),
    ('/transcribe2',Transcribe2)
], debug=True)
