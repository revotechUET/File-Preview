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
    env = os.getenv('ENV')
    budget_url = config['BUDGET_URL']['dev']
    if env == 'prod':
        budget_url = config['BUDGET_URL']['prod']
    res = requests.get(
        "{}/read-file/preview?file_path={}&service=WI_PROJECT_STORAGE".format(budget_url, requote_uri(params)), headers=headers, verify=False)
    return res
