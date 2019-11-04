import os
import sys


def ConvertFile(filename_input):
    filename_convert = filename_input.split('.')[0] + '.pdf'
    cmd = 'unoconv -f pdf --output=' + '\"' + filename_convert + \
        '\"' + ' ' + '\"' + filename_input + '\"'
    os.system(cmd.encode('utf-8'))
