import os
import datetime
import sys
import requests
import json
import traceback

serverUrl = 'http://ec2-54-169-111-88.ap-southeast-1.compute.amazonaws.com/api/receiveAd' 
custId = 1234
def get_latest_ads():
    resp = {}
    
    try:
        resp = requests.get(serverUrl, data=json.dumps({'custId': custId, 'city':'Chennai', 'region':'adyar'}))
        resp = json.loads(resp.text)
    except:
        print traceback.format_exc()
    return resp

def change_key_names():
    resp = get_latest_ads()
    resp = resp.get('Response')
    if not resp:
        return {}

change_key_names()
