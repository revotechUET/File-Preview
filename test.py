from convertFile import ConvertFile
from sendRequest import SendRequest
import json
import os


import requests


ROOT_DIR = os.path.dirname(os.path.abspath(
    __file__))  # This is your Project Root

headers = {'content-type': 'application/json', 'Authorization': "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6Imh1bmduayIsIndob2FtaSI6Im1haW4tc2VydmljZSIsInJvbGUiOjIsImNvbXBhbnkiOiJFU1MiLCJpYXQiOjE1NzIzNTMzNTgsImV4cCI6MTU3MzIxNzM1OH0.BR7grFeGBfs4He0-RxaQmKTMsqyQVdyWDCFQZsKV4fw",
           "Storage-Database": json.dumps({"directory": "344c5f0fb6ffc657590654fce9cafadd105a3f7e", "name": "ESS-hungnk", "company": "ESS"})}

params = '/IMG20161027131831.jpg'


file_name = params.split('/')[-1]

response = SendRequest(headers, params)
url = response.json()['url']
print(response.json())
print(type(url))
url_new = url.encode('utf-8')
print(type(url_new))
filedata = requests.get(url_new)
print(url)
print(filedata.status_code)
# ``filedata = urlopen(url)
# datatowrite = filedata.read()

# path_file_download = ROOT_DIR+'/uploads/' + file_name
# print(path_file_download)


# with open(path_file_download, 'wb') as f:
#     f.write(datatowrite)
# ConvertFile(path_file_download)

# url = "https://wi-storage-db-dev.s3.ap-southeast-1.amazonaws.com/ESS/344c5f0fb6ffc657590654fce9cafadd105a3f7e/T%C3%ACm%20hi%E1%BB%83u%20v%E1%BB%81%20H%E1%BB%8Dc%20b%E1%BB%95ng%20Mitsubishi.docx?AWSAccessKeyId=AKIAJNOXJXFO3CKGMBLA&Expires=1571945592&Signature=nCkh8U3D224yuv9CqBQwSpV4jQk%3D"
# print(url)
# r = requests.get(url)

# with open(ROOT_DIR+'/uploads/' + '1.docx', 'wb') as f:
#     f.write(r.content)
