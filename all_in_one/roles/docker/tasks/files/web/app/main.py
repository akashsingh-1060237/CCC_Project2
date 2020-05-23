from flask import Flask, jsonify, abort, make_response
import requests
import os
os.environ["HTTPS_PROXY"] = "http://wwwproxy.unimelb.edu.au:8000"
app = Flask(__name__)
urlfrmat='http://ip/dt'
url_corona='http://user:pass@localhost:5984/final_tweet_harvester2/_design/final/_view/corona?reduce=true&group=true'
url_economy='http://user:pass@localhost:5984/final_tweet_harvester2/_design/final/_view/economy?reduce=true&group=true'
url_employment='http://user:pass@localhost:5984/final_tweet_harvester2/_design/final/_view/employment?reduce=true&group=true'
url_hash_covid='http://user:pass@localhost:5984/final_tweet_harvester2/_design/final/_view/hashtag_covid?reduce=true&group=true'
url_hash_economy='http://user:pass@localhost:5984/final_tweet_harvester2/_design/final/_view/hashtag_economy?reduce=true&group=true'
url_hash_employment='http://user:pass@localhost:5984/final_tweet_harvester2/_design/final/_view/hashtag_employment?reduce=true&group=true'
url_location='http://user:pass@localhost:5984/final_tweet_harvester2/_design/final/_view/location?reduce=true&group=true'
url_precise='http://user:pass@localhost:5984/final_tweet_harvester2/_design/final/_view/precise?reduce=true&group=true'
rsp_corona=requests.get(url_corona)
rsp_economy=requests.get(url_economy)
rsp_employment=requests.get(url_employment)
rsp_hash_covid=requests.get(url_hash_covid)
rsp_hash_economy=requests.get(url_hash_economy)
rsp_hash_employment=requests.get(url_hash_employment)
rsp_location=requests.get(url_location)
rsp_precise=requests.get(url_precise)

print(rsp_corona.status_code)
print(rsp_economy.status_code)
print(rsp_employment.status_code)
print(rsp_hash_covid.status_code)
print(rsp_hash_economy.status_code)
print(rsp_hash_employment.status_code)
print(rsp_location.status_code)
print(rsp_precise.status_code)

content_corona = {}
content_economy = {}
content_employment = {}
content_hash_covid = {}
content_hash_economy = {}
content_hash_employment = {}
content_location = {}
content_precise = {}
try:
    content_corona=rsp_corona.json()
except:
    pass

try:
    content_economy=rsp_economy.json()
except:
    pass

try:
    content_employment=rsp_employment.json()
except:
    pass

try:
    content_hash_covid=rsp_hash_covid.json()
except:
    pass

try:
    content_hash_economy=rsp_hash_economy.json()
except:
    pass

try:
    content_hash_employment=rsp_hash_employment.json()
except:
    pass

try:
    content_location=rsp_location.json()
except:
    pass

try:
    content_precise=rsp_precise.json()
except:
    pass

@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify( { 'error': 'Bad request' } ), 400)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not found' } ), 404)

#datas = {"rows":[{"key":{"term":"covid","location":"melbourne"},"value": 1050 },
   # {"key":{"term":"economy","location":"sydney"},"value": 1100 }]}

#loc_data = {"rows":[{"key":{"location name":"10 savy road","location coordinates":[[[10.2,12.3],[14,13.9],[14.5,16.7],[18.9,20.1]]]},"value": 1050 },
   # {"key":{"location name":"10 portmelb road","location coordinates":[[[10.2,12.3],[14,13.9],[14.5,16.7],[18.9,20.1]]]},"value": 1200 }]}

def get_info(data):
    full_list = []
    info_list = data["rows"]
    for ind_info in info_list:
        info_dict = {}
        key_dict = ind_info["key"]
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
    return jsonify(list(get_info(content_corona)))

@app.route('/fetch/api/v1.0/tasks/economy', methods = ['GET'])
def get_tasks2():
    return jsonify(list(get_info(content_economy)))

@app.route('/fetch/api/v1.0/tasks/employment', methods = ['GET'])
def get_tasks3():
    return jsonify(list(get_info(content_employment)))

@app.route('/fetch/api/v1.0/tasks/hash_covid', methods = ['GET'])
def get_tasks4():
    return jsonify(list(get_info(content_hash_covid)))

@app.route('/fetch/api/v1.0/tasks/hash_economy', methods = ['GET'])
def get_tasks5():
    return jsonify(list(get_info(content_hash_economy)))

@app.route('/fetch/api/v1.0/tasks/hash_employment', methods = ['GET'])
def get_tasks6():
     return jsonify(list(get_info(content_hash_employment)))

@app.route('/fetch/api/v1.0/tasks/location', methods = ['GET'])
def get_tasks7():
    return jsonify(list(get_loc(content_location)))

@app.route('/fetch/api/v1.0/tasks/precise', methods = ['GET'])
def get_tasks8():
    return jsonify(list(get_loc_precise(content_precise)))


@app.route('/fetch/api/v1.0/tasks/<int:task_id>', methods = ['GET'])
def get_task(task_id):
    task = list(filter(lambda t: t['id'] == task_id, tasks))
    if len(task) == 0:
        abort(404)
    return jsonify( { 'task': make_public_task(task[0]) } )

@app.route("/")
def hello():
    return "Hello World"

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=80)