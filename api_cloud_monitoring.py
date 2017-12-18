"""
    CloudAPI -  Class/Methods to get information and reports overs diferents cloudproviders.
    Copyright (C) 2017  Carlos Smaniotto

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as
    published by the Free Software Foundation, either version 3 of the
    License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
from flask import Flask, request, Response, jsonify, make_response, url_for, abort
import json
from bson.json_util import dumps
from concurrent.futures import ThreadPoolExecutor
import os

import logging
from libs.cloud_wrapper import CloudWrapper
from libs.tools import convert_anything_to_bool
from config import log_config,  main_config

logging.config.dictConfig(log_config)
logging.getLogger(__name__)

TZ = main_config["system_timezone"]
logging.info("Setting the system timezone to {}".format(TZ))
os.environ['TZ'] = TZ

app = Flask(__name__)
executor = ThreadPoolExecutor(1)

global TEST_MODE
TEST_MODE = convert_anything_to_bool(os.getenv('TEST_MODE'))

def make_low_utilization(tag_key=None, tag_value=None):
    tag_key = None
    tag_value =  None
    cloud = CloudWrapper('aws')
    status = cloud.make_low_utilization(tag_key=tag_key, tag_value=tag_value, test_mode=TEST_MODE)
    logging.info("make_low_utilization has been finished!")

def get_low_utilization(tag_key=None, tag_value=None):
    pass

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Notfound' } ), 404)

@app.route('/')
def hello_world():
    return make_response(jsonify({'success': 'Cloud Mon API =)'}), 200)

@app.route('/routines/v1.0/lowutilization')
def run_make_low_utilization():
    executor.submit(make_low_utilization)
    return make_response(jsonify({'success': 'Running in Background and saving into DB...'}), 200)

@app.route('/api/v1.0/lowutilization',  methods = ['GET'])
def run_low_utilization():
    tag_key = request.args.get('tag_key')
    tag_value = request.args.get('tag_value')
    cloud = CloudWrapper('aws')
    obj = cloud.get_low_utilization_from_db(tag_key=tag_key, tag_value=tag_value)
    if obj is None:
        abort(404)
    obj_formatted = dumps(obj)
    response = Response(obj_formatted, status=200, mimetype='application/json')
    return response


if __name__ == '__main__':
    if TEST_MODE is True:
        print("TEST MODE ON")
        make_low_utilization()
    else:
        app.run(debug=True,  host='0.0.0.0', port=8080)
