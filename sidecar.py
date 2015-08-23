import hashlib
import hmac
import json
import requests

from datetime import datetime
from pytz import utc
from urlparse import urlparse

class Client:

    _methods_to_req_calls = {
            "GET": requests.get,
            "POST": requests.post,
            "PUT": requests.put,
            "DELETE": requests.delete
    }

    _sig_version = "1"

    def __init__(self, access_key, secret_key, base_url="http://api.sidecar.io/rest"):
        self._access_key = access_key
        self._secret_key = secret_key
        self._base_url = base_url

    def status(self):
        ep = self.base_url + "/status"
        resp = requests.get(ep)
        return json.loads(resp.content)["status"]

    def _make_authed_req(self, url, payload=None, method="GET"):
        headers = {}
        headers["Content-Type"] = "application/json"
        headers["Date"] = datetime.now(utc).isoformat()
        headers["Signature-Version"] = self._sig_version
        if payload is not None:
            headers["Content-MD5"] = _md5(payload)
        signature = self._sign_request(urlparse(url).path, headers["Date"], headers.get("Content-MD5"), method)
        headers["Authorization"] = "Sidecar " + self._access_key + ":" + signature
        req = self._methods_to_req_calls[method]
        return req(url=url, data=payload, headers=headers)


    def _sign_request(self, path, date, entity_md5, method="GET"):
        version = "1"
        md5 = entity_md5 if entity_md5 else ""
        to_sign = "\n".join([method, path, date, md5, version])
        return hmac.new(self._secret_key, to_sign, hashlib.sha1).hexdigest()

    def _md5(self, contents):
        return hashlib.md5(string).hexdigest()

    def _validate_user_auth(self):
        ep = self._base_url + "/v1/event/status"
        resp = self._make_authed_req(ep)
        return json.loads(resp.content)["status"]
