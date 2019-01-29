import os
import pip
import sys
import json
from pathlib import Path

URL = 'https://api.nasa.gov/planetary/apod'
apiKey = sys.argv[2]
imageFilePath = os.path.dirname(os.path.abspath(__file__)) + '/NASA_APOD.jpg'
hd = True

def InstallPIP():
    if pip.__version__ != '9.0.3':
        os.system('python -m pip install --upgrade pip==9.0.3')
        print('Downgrading the installed version of pip')

def ImportOrInstall(package):
    try:
        __import__(package)
    except ImportError:
        pip.main(['install', package])
        print('Installing ' + package)

def DeleteOldAPOD():
    imageFile = Path(imageFilePath)

    if imageFile.exists():
        os.remove(imageFilePath)
        print('Removing ' + imageFilePath)

def GetAPOD():
    ImportOrInstall('requests')

    import requests

    PARAMS = {
                'api_key': apiKey,
                'hd': hd
             }

    response = requests.get(url=URL, params=PARAMS)

    if response.status_code != 200:
        print('Error getting request from '+ URL)
        exit()

    print('Successfully got request from ' + URL)

    if hd:
        imgURL = json.loads(response.text)['hdurl']
    else:
        imgURL = json.loads(response.text)['url']

    imgResponse = requests.get(url=imgURL)

    if imgResponse.status_code != 200:
        print('Error getting request from ' + imgURL)
        exit()

    print('Successfully got request from ' + imgURL)

    with open(imageFilePath, 'wb') as f:
        f.write(imgResponse.content)

    del response
    del imgResponse

def SetDesktopBackground():
    ImportOrInstall('ctypes')

    import ctypes

    ctypes.windll.user32.SystemParametersInfoW(20, 0, imageFilePath, 0)
    print('Setting image as desktop background')

def main():
    InstallPIP()
    DeleteOldAPOD()
    GetAPOD()
    SetDesktopBackground()

if __name__ == '__main__':
    main()