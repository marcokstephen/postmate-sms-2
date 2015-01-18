import webapp2
import time
import twilio.twiml
import cgi
import urllib2
import json
import urllib

class ReceiveCall(webapp2.RequestHandler):
    def post(self):
        resp = twilio.twiml.Response()
        resp.say("Hello! Thank you for using our service. What is your street address? Press pound when you are finished.")
        resp.record(maxlength="30", action="/handle-recording0", transcribeCallback="/transcribe0")
        self.response.write(str(resp))

class ReceiveCall1(webapp2.RequestHandler):
    def post(self):
        resp = twilio.twiml.Response()
        resp.say("Thank you. What is the store that you would like to shop at? Press pound when you are finished.")
        resp.record(maxlength="30", action="handle-recording1", transcribeCallback="/transcribe1")
        self.response.write(str(resp))

class ReceiveCall2(webapp2.RequestHandler):
    def post(self):
        resp = twilio.twiml.Response()
        resp.say("Please list the items that you would like to buy. Press pound when you are finished.")
        resp.record(maxlength="30", action="handle-recording2", transcribeCallback="/transcribe2")
        self.response.write(str(resp))

class ReceiveCall3(webapp2.RequestHandler):
    def post(self):
        resp = twilio.twiml.Response()
        resp.say("Thank you, that will cost you ten thousand and five dollars. Goodbye")
        resp.hangup()
        self.response.write(str(resp))

class Transcribe0(webapp2.RequestHandler):
    def post(self):
        caller = cgi.escape(self.request.get('From'))
        message = cgi.escape(self.request.get('TranscriptionText'))

        url = "http://kenliao.me/pennapp/update.php?method=update&x=address&data="+urllib.quote(message)+"&number="+urllib.quote(caller)
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)

class Transcribe1(webapp2.RequestHandler):
    def post(self):
        caller = cgi.escape(self.request.get('From'))
        message = cgi.escape(self.request.get('TranscriptionText'))

        url = "http://kenliao.me/pennapp/update.php?method=update&x=store&data="+urllib.quote(message)+"&number="+urllib.quote(caller)
        request = urllib2.Request(url)
        response = urllib2.urlopen(request) 

class Transcribe2(webapp2.RequestHandler):
    def post(self):
        caller = cgi.escape(self.request.get('From'))
        message = cgi.escape(self.request.get('TranscriptionText'))

        url = "http://kenliao.me/pennapp/update.php?method=update&x=items&data="+urllib.quote(message)+"&number="+urllib.quote(caller)
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)

        url = "http://kenliao.me/pennapp/update.php?method=isfinished&number="+urllib.quote(caller)
        request = urllib2.request(url)
        response = urllib2.urlopen(request)

        while response == 0:
            time.sleep(3)
            response = urllib2.urlopen(request)
        
        #now we will do the api with the fields from response
		json_response = json.loads(response)
		address = json_response["address"]
		store = json_response["store"]
		items = json_response["items"]
		
		