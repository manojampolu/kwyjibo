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
    retDict = {'t1':"Live Sports Feed", 
                't1l1':resp.get("Live Sports Feed", {})[0][0], 
                't1l2':resp.get("Live Sports Feed", {})[0][1],
                't1l3':resp.get("Live Sports Feed", {})[0][2],
                't1l4':resp.get("Live Sports Feed", {})[0][3],
                't2':"Top News", 
                't2l1':resp.get('news', {}).get("Top News", {})[0],
                't2l2':resp.get('news', {}).get("Top News", {})[1],
                't2l3':resp.get('news', {}).get("Top News", {})[2],
                't2l4':resp.get('news', {}).get("Top News", {})[3],
                't3':"SENSEX", 
                't3l1':'BSE '+str(resp.get("stockMarket", {}).get("SENSEX", {}).get("current", 28000)),
                't3l2':'NSE '+str(resp.get("stockMarket", {}).get("NIFTY", {}).get("current", 8500)),
                't4':"Commodities", 
                't4l1':"Gold(10gm) "+str(resp.get("commodities", {}).get("gold", 30000)),
                't4l2':"Silver(1kg) "+str(resp.get("commodities", {}).get("silver", 47000)),
                't4l3':"1$ = Rs."+str(resp.get("commodities", {}).get("usdInr", 65)),
                'w1': resp.get("weather", {}).get("temp", 30),
                }
    tmpDict = dict([('img'+str(inx),val) for inx, val in enumerate(resp.get('ads'))])
    retDict.update(tmpDict)
    return retDict

print change_key_names()
