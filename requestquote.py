import json
import urllib2

class RequestQuote():
    @staticmethod
    def getquote():
        api_url = "https://api.postmates.com/v1/customers/cus_KAexnF0RCzFpck/delivery_quotes"
        pickup = "20 McAllister St, San Francisco, CA 94102"
        dropoff = "101 Market St, San Francisco, CA 94105"
        
        payload = {'dropoff_address': dropoff, 'pickup_address': pickup}
        req = urllib2.Request(api_url, urllib.urlencode(payload))
        base64string = base64.encodestring('25b9b722-0286-4747-aa1b-e369329b82d6:')[:-1]
        authheader =  "Basic %s" % base64string
        req.add_header("Authorization", authheader)

        response = urllib2.urlopen(req)
        json_response = response.read()
        json_output = json.loads(json_response)

        return json_output["fee"]
