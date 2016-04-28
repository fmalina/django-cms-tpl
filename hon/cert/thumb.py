"""
Make website thumbnails by rendering them in WebKit
http://cutycapt.sourceforge.net/

sudo apt-get install subversion libqt4-webkit libqt4-dev g++
svn co svn://svn.code.sf.net/p/cutycapt/code/ cutycapt
cd cutycapt/CutyCapt
qmake
make
./CutyCapt --url=http://medicinedict.com --out=medicinedict.png
"""

import os
import subprocess
import md5
from django.http import HttpResponse

CUTYCAPT = '/home/ubuntu/cutycapt/CutyCapt/CutyCapt'
THUMBS_DIR  = '/home/ubuntu/static/thumbs/'

def thumb(request, url):
    hash = md5.new(url).hexdigest()
    path = THUMBS_DIR + hash + '.png'
    # print path
    
    if not os.path.isfile(path):
        try:
            subprocess.check_call([CUTYCAPT,\
                '--url=' + url,\
                '--min-width=200',\
                '--out=' + path])
        except subprocess.CalledProcessError:
            return django.http.HttpResponseServerError
    
    img = open(path, 'rb').read()
    return django.http.HttpResponse(img, mimetype='image/png')