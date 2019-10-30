import json
import requests
import urllib


def SendRequest(headers, params):
    res = requests.get(
        "http://file-backend.dev.i2g.cloud/read-file/preview?file_path={}".format(urllib.quote_plus(params)), headers=headers, verify=False)
    return res
