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
        resp.say("Hello! Thank you for using our service. Please state your street address, then press pound.")
        resp.record(maxlength="30", action="/handle-recording0", transcribeCallback="/transcribe0")
        self.response.write(str(resp))

class ReceiveCall1(webapp2.RequestHandler):
    def post(self):
        resp = twilio.twiml.Response()
        resp.say("Thank you. What is the store that you would like to shop at? Press pound when finished.")
        resp.record(maxlength="30", action="handle-recording1", transcribeCallback="/transcribe1")
        self.response.write(str(resp))

class ReceiveCall2(webapp2.RequestHandler):
    def post(self):
        resp = twilio.twiml.Response()
        resp.say("Please list the items that you would like to buy, then press pound.")
        resp.record(maxlength="30", action="handle-recording2", transcribeCallback="/transcribe2")
        self.response.write(str(resp))

class ReceiveCall3(webapp2.RequestHandler):
    def post(self):
        resp = twilio.twiml.Response()
        resp.say("Thank you, your order will cost approximately $7.20 and is being placed. Goodbye.")
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
        request = urllib2.Request(url)

        time.sleep(10)
        response = urllib2.urlopen(request)
        json_response = json.loads(response)
	address = json_response[0]["address"]
	store = json_response[0]["store"]
	items = json_response[0]["items"]
		
	account_sid = "ACcdd722da9eb23c0be222908001c05621"
	auth_token  = "f42dc3d4155e275b7e6534a08d1c12fc"
	client = TwilioRestClient(account_sid, auth_token)
 
	message = client.messages.create(body="Sending "+items+" to "+address+".", to=caller, from_="+12673146567")
