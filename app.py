import os, sys, json, getopt
from flask import Flask, request, send_from_directory
from flask_cors import CORS, cross_origin
from datetime import datetime

from convertFile import ConvertFile
from sendRequest import SendRequest

import requests
import base64
import PyPDF2


ROOT_DIR = os.path.dirname(os.path.abspath(
    __file__))  # This is your Project Root

UPLOAD_FOLDER = '/mnt/z/Developer/Flask/uploads'

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:12345678@localhost/file_convert'
# db = SQLAlchemy(app)


# class FileConvert(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(200), nullable=False)
#     data = db.Column(db.LargeBinary)
#     date_created = db.Column(db. DateTime, default=datetime.utcnow)

#     def __repr__(self):
#         return '<FileConvert %r>' % self.id


@app.route("/filepreview", methods=['POST', 'GET'])
@cross_origin()
def file_preview():
    token = request.headers['Authorization']
    storage_database = request.headers['Storage-Database']

    headers = {'content-type': 'application/json', 'Authorization': token,
            "Storage-Database": storage_database}
    params = request.args.get('file_path')
    file_name = params.split('/')[-1]
    return get_cached_pdf(file_name, headers, params)
    # path_file_download = ROOT_DIR+'/uploads/' + file_name
# 
    # response = SendRequest(headers, params)
# 
    # url = response.json()['url']
    # filedata = requests.get(url)
# 
    # if filedata.status_code == 404:
        # return 'NOOO FILE PREVIEW'
# 
    # if filedata.status_code == 200:
        # with open(path_file_download, 'wb') as f:
            # f.write(filedata.content)
# 
    # ConvertFile(path_file_download)
    # file_name_convert = file_name.split('.')[0] + '.pdf'
# 
    # return base64.b64encode(open(ROOT_DIR+'/uploads/'+file_name_convert, "rb").read())


cached_pdf = []
CACHE_LIFE_TIME = 5 * 60
def get_cached_pdf(file_name, headers, params):
    file_name_convert = file_name.split('.')[0] + '.pdf'
    cached_item = next((item for item in cached_pdf if item['name'] == file_name_convert), None)
    path_file_converted = ROOT_DIR+'/uploads/'+file_name_convert
    if cached_item and (datetime.now() - cached_item['ts']).total_seconds() <= CACHE_LIFE_TIME:
        print((datetime.now() - cached_item['ts']).total_seconds())
        cached_item['ts'] = datetime.now()
        return base64.b64encode(open(path_file_converted, "rb").read())
    cached_item = {}
    path_file_download = ROOT_DIR+'/uploads/' + file_name
    response = SendRequest(headers, params)
    url = response.json()['url']
    filedata = requests.get(url)
    if filedata.status_code == 404:
        return 'NO FILE PREVIEW'
    if filedata.status_code == 200:
        with open(path_file_download, 'wb') as f:
            f.write(filedata.content)
    try:
        PyPDF2.PdfFileReader(open(path_file_download, "rb"))
    except PyPDF2.utils.PdfReadError:
        ConvertFile(path_file_download)
    else:
        path_file_converted = path_file_download
    cached_item['name'] = file_name_convert
    cached_item['ts'] = datetime.now()
    cached_pdf.append(cached_item)
    return base64.b64encode(open(path_file_converted, "rb").read())


def main(argv):
    port = 5000
    opts, args = getopt.getopt(argv,"hp:",["port="])
    if opts:
        print(opts)
        for opt, arg in opts:
            if opt in ("-p", "--port"):
                port = arg
    app.run(debug=True, host='0.0.0.0', port=port)


if __name__ == "__main__":
    main(sys.argv[1:])
