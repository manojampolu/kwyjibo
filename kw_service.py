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

app = Flask(__name__)
app.config["SECRET_KEY"] = 'adivik2000'
app.config['MONGO_DBNAME'] = "kwyjibo"
app.config['MONGO_USERNAME'] = "apache"
app.config['MONGO_PASSWORD'] = "apache123"
app.config['MONGO_HOST'] = "localhost"
app.config['MONGO_PORT'] = "27017"
app.config["SESSION_TYPE"] = 'footPryntSession'
CORS(app)
SESSION_USERID = 'customer'
#APP_URL = "http://ec2-54-179-145-237.ap-southeast-1.compute.amazonaws.com"

fp_mongo = PyMongo(app, config_prefix='MONGO')
env = Environment(app)

@app.route('/', methods=['GET'])
def hello():
    return "Hi you have landed on a live wire."


@app.route('/api/postAd', methods=['POST'])
def register():
    #customer can initiall register here
    if request.method == 'POST':
        try:
            regData = json.loads(request.get_data())
            fp_mongo.db.displayAds.insert(regData)
            return Response(json.dumps({'Response':'PostedAd'}), status=200, mimetype='application/json')
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
def register():
    #customer can initiall register here
    if request.method == 'GET':
        try:
            regData = json.loads(request.get_data())
            resp = get_ad_for_location(regData)
            return Response(json.dumps({'Response':resp}), status=200, mimetype='application/json')
        except:
            print traceback.format_exc()
    return bad_request('Incorrect request type. Try later.')

def get_ad_for_location(data):
    try:
        todayDate = str(datetime.date.today())
        location = data.get('location')
        ads = [i for i in fp_mongo.db.displayAds.find({'city':data.get('city'), 'region':data.get('region'), "validUpto": {"$lte": todayDate}, "validFrom": {"$gte": todayDate}})]
        return ads
    except:
        print traceback.format_exc()
        return []


if __name__ == "__main__":
    app.run(debug=True)
