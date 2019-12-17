import os
import sys
import json
import getopt
import requests
import base64
import PyPDF2
import jwt
import configparser
from flask import Flask, request
from flask_cors import CORS, cross_origin
from datetime import datetime
from convertFile import ConvertFile#, ConvertFileExcel
from sendRequest import SendRequest
from binaryornot.check import is_binary


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
MAX_SIZE = 10485760
config = configparser.ConfigParser()
config.read('config.ini')
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route("/filepreview", methods=['POST', 'GET'])
@cross_origin()
def file_preview():
    payload = request.get_json()
    item = payload['item']
    if item['size'] > MAX_SIZE:
        toReturn = {}
        toReturn['isTooBig'] = 1
        return toReturn
    else:
        token = request.headers['Authorization']
        decoded = jwt.decode(token, os.getenv('SECRET_KEY')
                             or config['SECRET_KEY']['key'])
        storage_database = request.headers['Storage-Database']
        headers = {'content-type': 'application/json', 'Authorization': token,
                   "Storage-Database": storage_database}
        file_path = item['path']
        return get_cached_pdf(headers, file_path, decoded)


@app.route("/refresh-cache", methods=['POST', 'GET'])
@cross_origin()
def refresh_cache():
    token = request.headers['Authorization']
    decoded = jwt.decode(token, os.getenv('SECRET_KEY')
                         or config['SECRET_KEY']['key'])
    cached_pdf[decoded['username']] = cached_pdf.get(decoded['username']) or []
    del cached_pdf[decoded['username']][:]
    return 'CACHE EMPTY'


cached_pdf = {}
CACHE_LIFE_TIME = 5 * 60


def get_cached_pdf(headers, file_path, decoded):
    file_name = file_path.replace('/', '__')
    file_name_convert = file_name + '.pdf'
    cached_pdf[decoded['username']] = cached_pdf.get(decoded['username']) or []
    cached_item = next(
        (item for item in cached_pdf[decoded['username']] if item['path'] == file_path), None)
    upload_folder_path = ROOT_DIR+'/uploads/' + decoded['username']
    if not os.path.exists(upload_folder_path):
        os.makedirs(upload_folder_path)
    path_file_converted = upload_folder_path + '/' + file_name_convert
    path_file_download = upload_folder_path + '/' + file_name
    if cached_item and (datetime.now() - cached_item['ts']).total_seconds() <= CACHE_LIFE_TIME:
        print((datetime.now() - cached_item['ts']).total_seconds())
        cached_item['ts'] = datetime.now()
        try:
            PyPDF2.PdfFileReader(open(path_file_download, "rb"))
        except PyPDF2.utils.PdfReadError:
            return base64.b64encode(open(path_file_converted, "rb").read())
        else:
            return base64.b64encode(open(path_file_download, "rb").read())
    cached_item = {}
    response = SendRequest(headers, file_path)
    url = response.json()['url']
    filedata = requests.get(url)
    if filedata.status_code == 404:
        return 'NO FILE PREVIEW'
    if filedata.status_code == 200:
        with open(path_file_download, 'wb') as f:
            f.write(filedata.content)
    if is_binary(path_file_download) and not path_file_download.lower().endswith(('jpg', 'JPG', 'png', 'PNG', 'jpeg', 'JPEG', 'gif', 'GIF',
                                                                                  'bmp', 'BMP', 'svg', 'SVG', 'pdf', 'las', 'asc', 'LAS', 'TXT',
                                                                                  'ASC', 'csv', 'CSV', 'xlsx', 'XLSX', 'XLS', 'xls', 'ppt', 'PPT',
                                                                                  'pptx', 'PPTX', 'doc', 'DOC', 'docx', 'DOCX')):
        return {'isNotReadable': 1}
    try:
        PyPDF2.PdfFileReader(open(path_file_download, "rb"))
    except PyPDF2.utils.PdfReadError:
        # if path_file_download.lower().endswith(('xlsx', 'xls', 'csv')):
            # ConvertFileExcel(path_file_download)
        # else:
        ConvertFile(path_file_download)
    else:
        path_file_converted = path_file_download
    cached_item['path'] = file_path
    cached_item['ts'] = datetime.now()
    cached_pdf[decoded['username']].append(cached_item)
    return base64.b64encode(open(path_file_converted, "rb").read())


def main(argv):
    port = 5000
    opts, args = getopt.getopt(argv, "hp:", ["port="])
    if opts:
        for opt, arg in opts:
            if opt in ("-p", "--port"):
                port = arg
    app.run(debug=True, host='0.0.0.0', port=port)


if __name__ == "__main__":
    main(sys.argv[1:])
