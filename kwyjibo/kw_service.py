import os
#os.environ['PYTHON_EGG_CACHE'] = '/usr/lib/python2.7/site-packages'
import sys
#! /usr/local/bin/python2.7
from flask import Flask, session, request, redirect, Response, current_app, render_template
from flask_pymongo import PyMongo
import json
import datetime
from flask_cors import CORS
from flask_bcrypt import check_password_hash, generate_password_hash
#from flask_mail import Mail, Message
import jwt
from functools import wraps
import traceback
import Geohash
from flask_assets import Environment
from bson import ObjectId
import sys
from argparse import ArgumentParser
from xml.dom import minidom
from collections import namedtuple
import re


try:
    from urllib.request import Request, urlopen
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlopen, urlencode
    from urllib2 import Request 

app = Flask(__name__)
app.config["SECRET_KEY"] = 'adivik2000'
app.config['MONGO_DBNAME'] = "kwyjibo"
#app.config['MONGO_USERNAME'] = "apache"
#app.config['MONGO_PASSWORD'] = "apache123"
app.config['MONGO_HOST'] = "localhost"
app.config['MONGO_PORT'] = "27017"
app.config["SESSION_TYPE"] = 'footPryntSession'
CORS(app)
SESSION_USERID = 'customer'
#APP_URL = "http://ec2-54-179-145-237.ap-southeast-1.compute.amazonaws.com"

fp_mongo = PyMongo(app, config_prefix='MONGO')
env = Environment(app)

class Encoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        else:
            return obj

@app.route('/', methods=['GET'])
def hello():
    return "Hi you have landed on a live wire."


@app.route('/api/postAd', methods=['POST'])
def post_ads():
    #customer can initiall register here
    if request.method == 'POST':
        try:
            regData = json.loads(request.get_data())
            fp_mongo.db.displayAds.insert(regData)
            return Response(json.dumps({'Response':'PostedAd'}, cls=Encoder), status=200, mimetype='application/json')
        except:
            print traceback.format_exc()
    return bad_request('Incorrect request type. Try later.')


@app.errorhandler(401)
def unauthorized(error=None):
    #standard 401 message
    message = {
            'status': 401,
            'message': 'Not Authorised',
    }
    return Response(json.dumps({'Response':message}), status=401, mimetype='application/json')

@app.errorhandler(400)
def bad_request(error=None):
    #standard 400 message
    message = {
            'status': 400,
            'message': error,
    }
    return Response(json.dumps({'Response':message}), status=400, mimetype='application/json')

@app.route('/api/receiveAd', methods=['GET'])
def get_ads():
    #customer can initiall register here
    if request.method == 'GET':
        try:
            regData = json.loads(request.get_data())
            resp = get_ad_for_location(regData)
            return Response(json.dumps({'Response':resp}, cls=Encoder), status=200, mimetype='application/json')
        except:
            print traceback.format_exc()
    return bad_request('Incorrect request type. Try later.')

def get_ad_for_location(data):
    resp = {}
    try:
        todayDate = str(datetime.date.today())
        location = data.get('location')
        #ads = [i for i in fp_mongo.db.displayAds.find({'city':data.get('city'), 'region':data.get('region'), "validUpto": {"$lte": todayDate}, "validFrom": {"$gte": todayDate}})]
        ads = [i for i in fp_mongo.db.displayAds.find({'city':data.get('city'), 'region':data.get('region')})]
        resp['ads'] = ads
        resp.update(get_latest_news())
        resp.update(get_weather(data.get('city')))
        resp.update(get_stock_updates())
        resp.update(get_gold_price())
    except:
        print traceback.format_exc()
    return resp

def get_weather(location):
    temp = {'weather': {'temp':30, 'condition':'Clear', 'wind_condition':'Wind: E at 16 mph', 'humidity':'Humidity: 59%'}}
    try:
        API_URL = "http://www.google.com/ig/api?"
        url = API_URL + urlencode({"weather": location})
        xml = urlopen(url).read().decode('utf-8', 'ignore').strip()
        print xml
        doc = minidom.parseString(xml.encode('utf-8'))
        forecast_information = doc.documentElement.getElementsByTagName("forecast_information")[0]
        city = forecast_information.getElementsByTagName("city")[0].getAttribute("data")

        current_conditions = doc.documentElement.getElementsByTagName("current_conditions")[0]
        temp = current_conditions.getElementsByTagName("temp_f" if args.unit == "F" else "temp_c")[0].getAttribute("data")
        condition = current_conditions.getElementsByTagName("condition")[0].getAttribute("data")
        wind_condition = current_conditions.getElementsByTagName("wind_condition")[0].getAttribute("data")
        humidity = current_conditions.getElementsByTagName("humidity")[0].getAttribute("data")
        temp = {'weather': {'temp':temp, 'condition':condition, 'wind_condition':'wind_condition', 'humidity':humidity}}
    except:
        print traceback.format_exc()
    return temp

def get_stock_updates():
    STOCK_CODE_LIST = [ "INDEXBOM:SENSEX", "NSE:NIFTY"]
    Stock = namedtuple("Stock", ["Index", "Current", "Change_pts", "Change_percent", "Updated_on"])
    stock = {'stockMarket':{"SENSEX":{'current':28000, 'changePoints':-104.91, 'changePercent':-0.36}, "NIFTY":{'current':8831, 'changePoints':-35.91, 'changePercent':-0.40}}}
    try:
        symbol_list = ','.join([st for st in STOCK_CODE_LIST])
        API_URL = 'http://finance.google.com/finance/info?client=ig&q='+symbol_list
        #req = Request(API_URL)
        resp = urlopen(API_URL)
        content = resp.read().decode('ascii', 'ignore').strip()
        content = content[3:]
        stock_resp_list = json.loads(content)
        for stock_resp in stock_resp_list:
            stock['stockMarket'][stock_resp["t"]] = {'current':stock_resp["l"],'changePoints':stock_resp["c"],'changePercent':stock_resp["lt"]}
        return stock
    except:
        print traceback.format_exc()
    return stock

def get_gold_price():
    GOLD_URL = "http://www.goldpriceindia.com/"
    SILVER_URL = "http://www.goldpriceindia.com/silver-price-india.php"
    comm = {'commodities': {"gold":30000, "silver":45000, "usdInr":65}}
    try:
        goldResp = urlopen(GOLD_URL).read()
        gold = goldResp.split("Today gold price in India is")[1][:15].replace(' ', '').replace('<b>', '').replace('</b>', '')
        usdInr = goldResp.split("US Dollar <i>to Rupee")[1][:15].replace(' ', '').replace('<u>', '').replace('</i>', '').replace('</b>', '')
        silverResp = urlopen(SILVER_URL).read()
        silver = silverResp.split('Today 1 KG silver price in India is')[1][:15].replace(' ', '').replace('<b>', '').replace('</b>', '')
        comm['commodities']["gold"] = gold
        comm['commodities']["silver"] = silver
        comm['commodities']["usdInr"] = usdInr
    except:
        print traceback.format_exc()
    return comm

def get_latest_news():
    news = {'headlines':[]}
    try:
        latest = urlopen("https://news.google.co.in/?edchanged=1&ned=ta_in&authuser=0").read()
        latest = [i for i in re.findall('href="(.+?)"', latest) if i.startswith('http') and ('thanthi' in i or 'vikatan' in i or 'tamil' in i or 'dinamani' in i)][:5]
        news['headlines'] = latest
    except:
        print traceback.format_exc()
    return news

if __name__ == "__main__":
    app.run(debug=True)
