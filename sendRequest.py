import json
import requests


def sendRequest(headers, params):
    res = requests.get("https://file-backend.i2g.cloud/read-file/preview",
                       params=params, headers=headers, verify=False)
    return res
