import os
import json
from flask import Flask, request, send_from_directory
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from convertFile import ConvertFile
from sendRequest import SendRequest

import requests


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
    params = request.args.get('file_path').encode('utf-8')
    file_name = params.split('/')[-1]
    path_file_download = ROOT_DIR+'/uploads/' + file_name

    response = SendRequest(headers, params)

    url = response.json()['url']
    filedata = requests.get(url)

    print(filedata.status_code)
    if filedata.status_code == 404:
        return 'NOOO FILE PREVIEW'

    if filedata.status_code == 200:
        with open(path_file_download, 'wb') as f:
            f.write(filedata.content)

    ConvertFile(path_file_download)
    file_name_convert = file_name.split('.')[0] + '.pdf'

    return open(ROOT_DIR+'/uploads/'+file_name_convert, "rb").read().encode("base64")


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
