import webapp2
import cgi
import twilio.twiml
import json
import apikeys
import urllib2

headers = {'X-Parse-Application-Id': apikeys.appID,
           'X-Parse-REST-API-Key': apikeys.restAPIkey,
           'Content-Type': 'application/json'}

tableURL = 'https://api.parse.com/1/classes/Transactions'


class ReceiveText(webapp2.RequestHandler):
    def get(self):
        self.response.write("you cant get bro, use post")

    def post(self):
        fromNumber = cgi.escape(self.request.get('From'))
        messageBody = cgi.escape(self.request.get('Body'))

        output = ''

        # check if there is a transaction
        r = urllib2.Request(tableURL + '?where={"number:' + str(fromNumber) + '"}', headers=headers)
        r = urllib2.urlopen(r).read()
        j = json.loads(r)
        
        if len(j['results']) == 0:   # new transaction
            data = {'number': fromNumber, 'state': 0}
            r = requests.post(tableURL, data=json.dumps(data), headers=headers)
            r = requests.get(tableURL + '/' + r.json()['objectId'], headers=headers)
        else:
            r = requests.get(j['objectId'], headers=headers)
            
            j = r.json()
            
        if j.state == 0:
            output = 'Hello! Welcome to Swift Squire! Where shall we deliver to?'
        elif j.state == 1:
            pass
        elif j.state == 2:
            pass
        elif j.state == 3:
            pass
        elif j.state == 4:
            pass
        elif j.state == 5:
            pass
        else:
            output = 'BADNESS'
           
        resp = twilio.twiml.Response()
        resp.message("hello")
        self.response.write(str(resp))

        
