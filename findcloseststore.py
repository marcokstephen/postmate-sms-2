import json
import requests
import urllib

class FindClosest():
    @staticmethod
    def findclosest():
        keyword = "Walmart"
        current_address = "201-269 S 36th St, Philadelphia, PA 19104, USA"

        api_url = "https://maps.googleapis.com/maps/api/geocode/json?address="+urllib.quote(current_address)+"&key=AIzaSyBTsBPcS2k5L9kCXUW0qnbT3M0vadHrspU"
        r = requests.get(api_url)
        lat_json_obj = json.loads(r.text)
        lat = lat_json_obj["results"][0]["geometry"]["location"]["lat"]
        long = lat_json_obj["results"][0]["geometry"]["location"]["lng"]

        api_url = "https://maps.googleapis.com/maps/api/place/textsearch/json?query="+urllib.quote(keyword)+"&key=AIzaSyBTsBPcS2k5L9kCXUW0qnbT3M0vadHrspU&location="+str(lat)+","+str(long)+"&radius=1"
        r = requests.get(api_url)
        json_result = json.loads(r.text)
        return json_result["results"][0]["formatted_address"]
