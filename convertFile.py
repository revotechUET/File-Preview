import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def ConvertFile(filename_input):
    filename_convert = filename_input.split('.')[0] + '.pdf'
    print(filename_convert)
    cmd = 'unoconv -f pdf --output=' + '\"' + filename_convert + \
        '\"' + ' ' + '\"' + filename_input + '\"'
    os.system(cmd.encode('utf-8'))
