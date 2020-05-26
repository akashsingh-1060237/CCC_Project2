from flask import Flask, jsonify, abort, make_response
import requests
from flask_cors import CORS
# import os
# os.environ["HTTPS_PROXY"] = "http://wwwproxy.unimelb.edu.au:8000"
app = Flask(__name__)
CORS(app)
urlfrmat='http://ip/dt'
url_corona='http://user:pass@127.0.0.1:5984/final_tweet_harvester2/_design/final/_view/corona?reduce=true&group=true'
url_economy='http://user:pass@127.0.0.1:5984/final_tweet_harvester2/_design/final/_view/economy?reduce=true&group=true'
url_employment='http://user:pass@127.0.0.1:5984/final_tweet_harvester2/_design/final/_view/employment?reduce=true&group=true'
url_hash_covid='http://user:pass@127.0.0.1:5984/final_tweet_harvester2/_design/final/_view/hashtag_covid?reduce=true&group=true'
url_hash_economy='http://user:pass@127.0.0.1:5984/final_tweet_harvester2/_design/final/_view/hashtag_economy?reduce=true&group=true'
url_hash_employment='http://user:pass@127.0.0.1:5984/final_tweet_harvester2/_design/final/_view/hashtag_employment?reduce=true&group=true'
url_location='http://user:pass@127.0.0.1:5984/final_tweet_harvester2/_design/final/_view/location?reduce=true&group=true'
url_precise='http://user:pass@127.0.0.1:5984/final_tweet_harvester2/_design/final/_view/precise?reduce=true&group=true'

loc_list = ['Sydney', 'Melbourne', 'Brisbane', 'Perth', 'Adelaide',
'Gold Coast', 'Canberra', 'Newcastle', 'Wollongong', 'Logan City', 'Geelong', 'Hobart', 'Townsville',
'Cairns', 'Toowoomba', 'Darwin', 'Rockingham', 'Launceston', 'Bendigo', 'Ballarat', 'Mandurah', 'Mackay',
'Bundaberg', 'Bunbury', 'Maitland', 'Armadale', 'Rockhampton','Adelaide Hills', 'South Brisbane', 'Hervey Bay']

@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify( { 'error': 'Bad request' } ), 400)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not found' } ), 404)

def get_info(data):
    full_list = []
    info_list = data["rows"]
    for ind_info in info_list:
        info_dict = {}
        key_dict = ind_info["key"]
        if key_dict["location"] in loc_list:
            info_dict["term"] = key_dict["term"]
            info_dict["location"] = key_dict["location"]
            info_dict["count"] = ind_info["value"]
            full_list.append(info_dict)
    return full_list

def get_loc(data):
    full_list = []
    info_list = data["rows"]
    for ind_info in info_list:
        info_dict = {}
        key_dict = ind_info["key"]
        if key_dict["location name"] in loc_list:
            info_dict["location name"] = key_dict["location name"]
            info_dict["location coordinates"] = key_dict["location coordinates"][0]
            info_dict["count"] = ind_info["value"]
            full_list.append(info_dict)
    return full_list

def get_loc_precise(data):
    full_list = []
    info_list = data["rows"]
    for ind_info in info_list:
        info_dict = {}
        key_dict = ind_info["key"]
        info_dict["location name"] = key_dict["location name"]
        info_dict["location coordinates"] = key_dict["location coordinates"]
        info_dict["count"] = ind_info["value"]
        full_list.append(info_dict)
    return full_list

@app.route('/fetch/api/v1.0/tasks/corona', methods = ['GET'])
def get_tasks1():
    response = jsonify(list(get_info(requests.get(url_corona).json())))
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/fetch/api/v1.0/tasks/economy', methods = ['GET'])
def get_tasks2():
    return jsonify(list(get_info(requests.get(url_economy).json())))

@app.route('/fetch/api/v1.0/tasks/employment', methods = ['GET'])
def get_tasks3():
    return jsonify(list(get_info(requests.get(url_employment).json())))

@app.route('/fetch/api/v1.0/tasks/hash_covid', methods = ['GET'])
def get_tasks4():
    return jsonify(list(get_info(requests.get(url_hash_covid).json())))

@app.route('/fetch/api/v1.0/tasks/hash_economy', methods = ['GET'])
def get_tasks5():
    return jsonify(list(get_info(requests.get(url_hash_economy).json())))

@app.route('/fetch/api/v1.0/tasks/hash_employment', methods = ['GET'])
def get_tasks6():
     return jsonify(list(get_info(requests.get(url_hash_employment).json())))

@app.route('/fetch/api/v1.0/tasks/location', methods = ['GET'])
def get_tasks7():
    return jsonify(list(get_loc(requests.get(url_location).json())))

@app.route('/fetch/api/v1.0/tasks/precise', methods = ['GET'])
def get_tasks8():
    return jsonify(list(get_loc_precise(requests.get(url_precise).json())))

if __name__ == '__main__':
    app.run(debug = True, host = '0.0.0.0', port = 80)