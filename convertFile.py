import os
import sys
import requests
import json
# import excel2img
# import img2pdf

uploadUrl = 'https://products.aspose.app/tasks/api/FileManager/UploadFile'
convertUrl = 'https://products.aspose.app/tasks/api/TasksConversion/Convert'
downloadUrl = 'https://products.aspose.app/tasks/api/FileManager/DownloadFile'


def ConvertFile(filename_input):
    if filename_input.lower().endswith('mpp'):
        print('inside convert func', filename_input)
        mppReadFile = open(filename_input, 'rb')
        files = {
            'TasksConversion': mppReadFile
        }
        try:
            res1 = requests.post(uploadUrl, files=files)
            if res1.status_code != 200:
                raise Exception("Cann\'t get upload ID")
            uploadId = str(res1.text).replace("\"", "")
            print('uploadId', uploadId)
            convertHeaders = {"Content-Type": "application/json"}
            body = {
                "fileGuid": uploadId,
                "fileFormat": "PDF"
            }
            # body = json.dumps(body)
            # print(type(body))
            # print(body)
            res2 = requests.post(convertUrl, json=body)
            print(res2.content)
            if res2.status_code != 200:
                raise Exception("Cann\'t get download ID")
            downloadId = str(res2.text).replace("\"", "")
            print('downloadId', downloadId)
            res3 = requests.get(downloadUrl + '/' + downloadId)
            if res3.headers['Content-Type'] == 'application/octet-stream':
                print('OCTET')
                with open(filename_input + '.pdf', 'wb') as f:
                    f.write(res3.content)
            else:
                raise Exception("Cann\'t convert file")
        except Exception as error:
            print(error)
    else:
        filename_convert = filename_input + '.pdf'
        cmd = 'unoconv -f pdf --output=' + '\"' + filename_convert + \
            '\"' + ' ' + '\"' + filename_input + '\"'
        os.system(cmd.encode('utf-8'))


# def ConvertFileExcel(filename_input):
    # excel2img.export_img('{}'.format(filename_input),
        # '{}.png'.format(filename_input))
#
    # with open("{}.pdf".format(filename_input), "wb") as f:
        # f.write(img2pdf.convert('{}.png'.format(filename_input)))
