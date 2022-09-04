# coding=utf-8

import sys
sys.path.append("/opt/midware/imageserver/lib/lib/python3.8/site-packages")
import requests

url = 'http://127.0.0.1:9081/matimage'
def getimage():
    xdata = range(1, 6)
    ydata = range(11, 16)
    params = {"xdata": list(xdata), "ydata": list(ydata)}
    try:
        res = requests.get(url, params=params)
        code = res.status_code
        img = res.text
    except requests.exceptions.ConnectionError as e:
        # print(e)
        code = 404
        img = ""
    # print(res.content)
    return code, img

if __name__ == '__main__':
    print("--" * 100)
    code = getimage()
    print(code)