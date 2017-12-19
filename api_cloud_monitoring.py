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

import os
import configparser

dir_path = os.path.dirname(os.path.realpath(__file__))
config_ini = "{}/api_config.ini".format(dir_path)
os.environ['CONFIG'] = config_ini
config = configparser.ConfigParser()
config.read(config_ini)



from flask import Flask, request, Response, jsonify, make_response, url_for, abort
import json
from bson.json_util import dumps
from concurrent.futures import ThreadPoolExecutor

import logging
from libs.cloud_wrapper import CloudWrapper
from libs.tools import convert_anything_to_bool
from config import log_config

# Get from  linux environment the variable TEST_MODE, case exist it'll define if the API will running in test mode
global TEST_MODE
TEST_MODE = convert_anything_to_bool(os.getenv('TEST_MODE'))

# CONFIG API from config.ini

api_config = config['api']
monitoring_config = config['monitoring']

TZ = api_config.get('timezone', fallback='UTC')
API_DEBUG = api_config.getboolean('debug', fallback=False)
LISTINER_IP = api_config.get('listner_ip', fallback='0.0.0.0')
LISTINER_PORT = api_config.getint('listner_port', fallback=8080)

os.environ['TZ'] = TZ
logging.config.dictConfig(log_config)
logging.getLogger(__name__)

app = Flask(__name__)
executor = ThreadPoolExecutor(1)


def make_low_utilization(tag_key=None, tag_value=None, max_cpu=None, max_availiableemory=None, network=None):
    tag_key = None
    tag_value = None

    if max_cpu is None or max_availiableemory is None or network is None:
        max_cpu = monitoring_config.getfloat('max_cpu_pct', fallback=50)
        max_mem_available = monitoring_config.getfloat('max_mem_availiable_pct', fallback=50)
        network = monitoring_config.getint('min_network_io_period_mb', fallback=150)

    cloud = CloudWrapper('aws')
    status = cloud.make_low_utilization(tag_key=tag_key, tag_value=tag_value, max_cpu=max_cpu,
                                        max_mem_available=max_mem_available, network=network, test_mode=TEST_MODE)
    logging.info("make_low_utilization has been finished!")


def get_low_utilization(tag_key=None, tag_value=None):
    pass


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Notfound'}), 404)


@app.route('/')
def hello_world():
    return make_response(jsonify({'success': 'Cloud Mon API =)'}), 200)


@app.route('/routines/v1.0/lowutilization')
def run_make_low_utilization():
    executor.submit(make_low_utilization)
    return make_response(jsonify({'success': 'Running in Background and saving into DB...'}), 200)


@app.route('/api/v1.0/lowutilization', methods=['GET'])
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
        app.run(debug=API_DEBUG, host=LISTINER_IP, port=LISTINER_PORT)
