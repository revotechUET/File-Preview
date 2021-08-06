import os
import sys
import requests
import json
import pdfkit
# import excel2img
# import img2pdf

#replace with mpp service's IP and port
uploadUrl = 'http://192.168.1.15:8080/tasks/api/FileManager/UploadFile'
convertUrl = 'http://192.168.1.15:8080/tasks/api/TasksConversion/Convert'
downloadUrl = 'http://192.168.1.15:8080/tasks/api/FileManager/DownloadFile'


def ConvertFile(filename_input):
    if filename_input.lower().endswith('mpp'):
        print('inside convert func', filename_input)
        mppReadFile = open(filename_input, 'rb')
        
        files = {
            'file': mppReadFile,
        }

        try:
            res1 = requests.post(uploadUrl, files=files, params={'api-key': 'MY_API_KEY'})
            print(res1.status_code)
            if res1.status_code != 200:
                raise Exception("Unable to get uploadId")
            uploadId = res1.json()["message"]
            print('uploadId', uploadId)
            
            body = {
                "fileGuid": uploadId,
                "format": "HTML"
            }
            res2 = requests.post(convertUrl, json=body)
            if res2.status_code != 200:
                raise Exception("Something wrong")
            res3 = requests.get(downloadUrl + '/' + uploadId)
            with open(filename_input + '.html', 'w') as f:
                f.write(res3.content.decode('utf8'))
            pdfkit.from_file(filename_input + '.html', filename_input + '.pdf')
        except Exception as error:
            print("try/catch", error)
    else:
        filename_convert = filename_input + '.pdf'
        cmd = 'unoconv -f pdf --output=' + '\"' + filename_convert + \
            '\"' + ' ' + '\"' + filename_input + '\"'
        os.system(cmd.encode('utf-8'))