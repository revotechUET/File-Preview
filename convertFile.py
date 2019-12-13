import os
import sys
import excel2img


def ConvertFile(filename_input):
    filename_convert = filename_input + '.pdf'
    cmd = 'unoconv -f pdf --output=' + '\"' + filename_convert + \
        '\"' + ' ' + '\"' + filename_input + '\"'
    os.system(cmd.encode('utf-8'))


def ConvertFileExcel(filename_input):
    excel2img.export_img('{}'.format(filename_input),
                         '{}.png'.format(filename_input))
