import json
import requests

class RequestQuote():
    @staticmethod
    def getquote():
        api_url = "https://api.postmates.com/v1/customers/cus_KAexnF0RCzFpck/delivery_quotes"
        pickup = "20 McAllister St, San Francisco, CA 94102"
        dropoff = "101 Market St, San Francisco, CA 94105"

        payload = {'dropoff_address': dropoff, 'pickup_address': pickup}
        r = requests.post(api_url, auth=('25b9b722-0286-4747-aa1b-e369329b82d6', ''), data=payload)
        json_output = json.loads(r.text)

        return json_output["fee"]
