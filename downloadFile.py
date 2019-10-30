import os
from urllib.request import urlopen

ROOT_DIR = os.path.dirname(os.path.abspath(
    __file__))  # This is your Project Root
filedata = urlopen('http://i3.ytimg.com/vi/J---aiyznGQ/mqdefault.jpg')
datatowrite = filedata.read()

with open(ROOT_DIR+'\\uploads\\cat.png', 'wb') as f:
    f.write(datatowrite)


print(ROOT_DIR)
