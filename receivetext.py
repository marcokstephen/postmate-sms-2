import webapp2
import cgi
import twilio.twiml
import json
import apikeys
import urllib2
import urllib
import base64
import dateutil.parser
import datetime
import time
from google.appengine.api import taskqueue
from findcloseststore import FindClosest


headers = {'X-Parse-Application-Id': apikeys.appID,
           'X-Parse-REST-API-Key': apikeys.restAPIkey,
           'Content-Type': 'application/json'}

tableURL = 'https://api.parse.com/1/classes/Transactions'
apikeys.pm_url_quote = "https://api.postmates.com/v1/customers/"+apikeys.pm_customerID+"/delivery_quotes"
base64string = base64.encodestring('%s:%s' % (apikeys.pm_appID, "")).replace('\n', '')


class ReceiveText(webapp2.RequestHandler):
    def upstate(self, state, objId):
        # change state
        opener = urllib2.build_opener(urllib2.HTTPHandler)
        DAJSON = {"state": state}
        request = urllib2.Request(tableURL + '/' + objId, json.dumps(DAJSON), headers=headers)
        request.get_method = lambda: 'PUT'
        opener.open(request)

    def get(self):
        self.response.write("you cant get bro, use post")

    def post(self):
        fromNumber = cgi.escape(self.request.get('From'))
        messageBody = cgi.escape(self.request.get('Body'))

        output = ''

        objId = 0

        # check if there is a transaction
        r = urllib2.Request(tableURL + '?where={"number":' + str(fromNumber) + '}', headers=headers)
        r = urllib2.urlopen(r).read()
        j = json.loads(r)

        if len(j['results']) == 0:  # new transaction
            data = {'number': int(fromNumber), 'state': 0}
            r = urllib2.Request(tableURL, data=json.dumps(data), headers=headers)
            r = urllib2.urlopen(r).read()
            j = json.loads(r)
            objId = j['objectId']
            j['state'] = 0
        else:                   # transaction is found
            r = urllib2.Request(tableURL + '/' + j['results'][0]['objectId'], headers=headers)
            r = urllib2.urlopen(r).read()
            j = json.loads(r)
            objId = j['objectId']

        if j['state'] == 0:
            output = 'Hello! Welcome to Swift Squire Courier Service! Where shall we deliver to?'
            self.upstate(1, objId)

        elif j['state'] == 1:
            opener = urllib2.build_opener(urllib2.HTTPHandler)
            DAJSON = {"whereto": messageBody}
            request = urllib2.Request(tableURL + '/' + objId, json.dumps(DAJSON), headers=headers)
            request.get_method = lambda: 'PUT'
            opener.open(request)

            output = 'At which store would you like to purchase merchandise?'
            self.upstate(2, objId)

        elif j['state'] == 2:
            opener = urllib2.build_opener(urllib2.HTTPHandler)
            DAJSON = {"storename": messageBody}
            request = urllib2.Request(tableURL + '/' + objId, json.dumps(DAJSON), headers=headers)
            request.get_method = lambda: 'PUT'
            opener.open(request)
            
            r = urllib2.Request(tableURL+'/'+objId, headers=headers)
            r = urllib2.urlopen(r).read()
            j = json.loads(r)
            wherefrom = FindClosest().findclosest(messageBody, j['whereto'])

            opener = urllib2.build_opener(urllib2.HTTPHandler)
            DAJSON = {"wherefrom": wherefrom}
            request = urllib2.Request(tableURL + '/' + objId, json.dumps(DAJSON), headers=headers)
            request.get_method = lambda: 'PUT'
            opener.open(request)

            output = 'What would you like to purchase?'
            self.upstate(3, objId)

        elif j['state'] == 3:
            opener = urllib2.build_opener(urllib2.HTTPHandler)
            DAJSON = {"whatbuy": messageBody}
            request = urllib2.Request(tableURL + '/' + objId, json.dumps(DAJSON), headers=headers)
            request.get_method = lambda: 'PUT'
            opener.open(request)

            r = urllib2.Request(tableURL+'/'+objId, headers=headers)
            r = urllib2.urlopen(r).read()
            j = json.loads(r)

            deliver_address = j['wherefrom']
            pickup_address = j['whereto']

            addr_data = {'dropoff_address': deliver_address, 
                         'pickup_address': pickup_address}

            r = urllib2.Request(apikeys.pm_url_quote, data=urllib.urlencode(addr_data))
            r.add_header("Authorization", "Basic %s" % base64string)
            r = urllib2.urlopen(r).read()
            qt = json.loads(r)

            opener = urllib2.build_opener(urllib2.HTTPHandler)
            DAJSON = {"Qid": qt['id']}
            request = urllib2.Request(tableURL + '/' + objId, json.dumps(DAJSON), headers=headers)
            request.get_method = lambda: 'PUT'
            opener.open(request)

            opener = urllib2.build_opener(urllib2.HTTPHandler)
            DAJSON = {"duration": qt['duration']}
            request = urllib2.Request(tableURL + '/' + objId, json.dumps(DAJSON), headers=headers)
            request.get_method = lambda: 'PUT'
            opener.open(request)

            output = 'Confirmation: purchasing ' + j['whatbuy'] + ' from ' + j['storename'] + \
                     ' at ' + j['wherefrom'] + ' to the destination ' + j['whereto'] + \
                     ' costing $' + str(format(qt['fee'] * 0.01, '.2f')) + '. Reply "yes" to confirm.'

            self.upstate(4, objId)

        elif j['state'] == 4:
            # output = 'updates for you impatient soul'
            if messageBody.strip().lower() == 'yes':
                output = 'Order confirmed! Reply "update" for a delivery update'
                self.upstate(5, objId)
            else:
                output = 'Order cancelled'
                
                opener = urllib2.build_opener(urllib2.HTTPHandler)
                request = urllib2.Request(tableURL + '/' + objId, headers=headers)
                request.get_method = lambda: 'DELETE'
                opener.open(request)
            
        elif j['state'] == 5:
            s = j['updatedAt']
            d = dateutil.parser.parse(s)
            d = d.astimezone(dateutil.tz.tzutc())
            d1_t = time.mktime((d + datetime.timedelta(minutes=j['duration'])).timetuple())
            d2_t = time.mktime(datetime.datetime.now().timetuple())
            min = int(int(d1_t-d2_t) / 60)
            output = str(min) + ' minutes remaining'
            
            # self.upstate(6)
        else:
            output = 'BADNESS'

        resp = twilio.twiml.Response()
        resp.message(output)
        self.response.write(str(resp))


