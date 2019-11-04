import json
import requests
import os
import configparser
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from requests.utils import requote_uri


config = configparser.ConfigParser()
config.read('config.ini')


def SendRequest(headers, params):
    budget_url = os.getenv('BUDGET_URL') or config['BUDGET_URL']['url'] or "https://users.i2g.cloud"
    service_name = ""
    if os.getenv('SERVICE'):
        service_name = "&service={}".format(os.getenv('SERVICE'))
    res = requests.get(
        "{}/read-file/preview?file_path={}{}".format(budget_url, requote_uri(params), service_name), headers=headers, verify=False)
    return res
