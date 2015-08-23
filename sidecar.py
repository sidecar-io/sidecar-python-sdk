import requests
import json

class Client:
  
    def __init__(self, access_key, secret_key, base_url="http://api.sidecar.io/rest"):
        self.access_key = access_key
        self.secret_key = secret_key
        self.base_url = base_url

    def status(self):
        status_ep = self.base_url + "/status"
        resp = requests.get(status_ep)
        return json.loads(resp.content)["status"]
        

