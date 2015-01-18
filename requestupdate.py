import urllib
import urllib2
import json
import webapp2
import base64

class RequestUpdate(webapp2.RequestHandler):
    @staticmethod
    def getstatus():
        delivery_id = "del_K7SD1dUd5aqLU-"
        api_url = "https://api.postmates.com/v1/customers/cus_KAexnF0RCzFpck/deliveries/"+urllib.quote(delivery_id)

        base64string = base64.encodestring('25b9b722-0286-4747-aa1b-e369329b82d6:')[:-1]
        authheader =  "Basic %s" % base64string
        req = urllib2.Request(api_url)
        req.add_header("Authorization", authheader)

        response = urllib2.urlopen(req)
        json_response = response.read()
        json_output = json.loads(json_response)

        return json_output

