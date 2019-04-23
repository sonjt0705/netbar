# Python 3.7 is required!
import json
import os
import sys
import urllib.request

appcId = None
appcPw = None

with open('id.appc', 'r') as fp:
    appcId = fp.read()

with open('pw.appc', 'r') as fp:
    appcPw = fp.read()

taskCode = '0'
APIURL = 'https://openapi.naver.com/v1/captcha/nkey?code=' + taskCode

req = urllib.request.Request(APIURL)
req.add_header('X-Naver-Client-Id', appcId)
req.add_header('X-Naver-Client-Secret', appcPw)
res = urllib.request.urlopen(req)
resCode = res.getcode()
if resCode == 200:
    resBody = json.loads(res.read().decode('utf-8'))
    cKey = resBody['key']
else:
    print('Error: ' + resCode)
    exit(-1)

APIURL = 'https://openapi.naver.com/v1/captcha/ncaptcha.bin?key=' + cKey
req = urllib.request.Request(APIURL)
req.add_header('X-Naver-Client-Id', appcId)
req.add_header('X-Naver-Client-Secret', appcPw)
res = urllib.request.urlopen(req)
resCode = res.getcode()
if resCode == 200:
    resBody = res.read()
    with open('captcha.jpg', 'wb') as fp:
        fp.write(resBody)
else:
    print('Error: ' + resCode)
    exit(-1)

taskCode = '1'
cValue = input('cv > ')
APIURL = 'https://openapi.naver.com/v1/captcha/nkey?code=' + taskCode + '&key=' + cKey + '&value=' + cValue
req = urllib.request.Request(APIURL)
req.add_header('X-Naver-Client-Id', appcId)
req.add_header('X-Naver-Client-Secret', appcPw)
res = urllib.request.urlopen(req)
resCode = res.getcode()
if resCode == 200:
    resBody = json.loads(res.read().decode('utf-8'))
    if resBody['result']: print('You are good!')
    else: print('You are bad!')
    print(resBody['responseTime'])
else:
    print('Error: ' + resCode)
    exit(-1)

print('The end')
exit(0)
