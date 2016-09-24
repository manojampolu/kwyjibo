import os
import datetime
import sys
import requests
import json

serverUrl = 'http://ec2-54-169-111-88.ap-southeast-1.compute.amazonaws.com/api/receiveAd' 
custId = 1234
def get_latest_ads():
    try:
        resp = requests.post(serverUrl, data=json.dumps({'custId': custId}))
        resp = json.loads(resp)
    except:
        print traceback.format_exc()
