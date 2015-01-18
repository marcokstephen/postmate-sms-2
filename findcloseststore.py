import json
import urllib2
import urllib

class FindClosest():
    @staticmethod
    def findclosest():
        keyword = "Walmart"
        current_address = "201-269 S 36th St, Philadelphia, PA 19104, USA"

        api_url = "https://maps.googleapis.com/maps/api/geocode/json?address="+urllib.quote(current_address)+"&key=AIzaSyBTsBPcS2k5L9kCXUW0qnbT3M0vadHrspU"
        request = urllib2.Request(api_url)
        response = urllib2.urlopen(request)
        json_result = response.read()
        lat_json_obj = json.loads(json_result)
        lat = lat_json_obj["results"][0]["geometry"]["location"]["lat"]
        long = lat_json_obj["results"][0]["geometry"]["location"]["lng"]

        api_url = "https://maps.googleapis.com/maps/api/place/textsearch/json?query="+urllib.quote(keyword)+"&key=AIzaSyBTsBPcS2k5L9kCXUW0qnbT3M0vadHrspU&location="+str(lat)+","+str(long)+"&radius=1"
        request = urllib2.Request(api_url)
        response = urllib2.urlopen(request)
        json_result = response.read()
        json_result = json.loads(json_result)
        return json_result["results"][0]["formatted_address"]
