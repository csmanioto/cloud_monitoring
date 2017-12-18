"""
    config.py - Dict with key/value used into the class and others pice os the project
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


main_config = {
    "system_pidfile": "cloud_monitoring.pid",
    "system_percent_max_cpu": 50,
    "system_percent_max_availiableemory": 50,
    "network_io_mega": 150,
    "system_timezone": "UTC",
    "system_ssh_timeout": 2,
    "system_ntp_server": "0.north-america.pool.ntp.org, 1.north-america.pool.ntp.org, 2.north-america.pool.ntp.org, 3.north-america.pool.ntp.org",
    "system_loglevel": "DEBUG",
    "system_logfile": None,
    "system_test_mode": True, # When true, don't running into cloud and don't save into db and use pick file as data instead of aws api
    "system_test_mode_ids": [
                                {'id': 'i-0aeb5dcc19892e8a6',   'region': 'us-east-1'},
                                {'id': 'i-0349b84be2af801c4',	'region': 'sa-east-1'},
                                {'id': 'i-07e942ad6c0796443',	'region': 'sa-east-1'},
                                {'id': 'i-02c0532f015927db4',	'region': 'sa-east-1'},
                                {'id': 'i-075212272e7a51ab9',	'region': 'sa-east-1'},
                                {'id': 'i-028103819d9998954',	'region': 'sa-east-1'},
                                {'id': 'i-0e44316a6217e7d58',	'region': 'sa-east-1'},
                                {'id': 'i-07e5c2f095f72af6e', 	'region': 'sa-east-1'},
                                {'id': 'i-0349b84be2af801c4',  	'region': 'sa-east-1'}
                            ],
    "aws_regions": ['us-east-1','us-west-1','us-west-2','eu-west-1','sa-east-1', 'ap-southeast-1','ap-southeast-2','ap-northeast-1'],
    "aws_ssh_key_folder": "/Volumes/DataDisk/csmaniotto/projects/pemkeys/",

    "mongo-server": "localhost:27017",
    "mongo_db-": "clound_mon",
    "mongo_collection": "???_low_utilization",

    "rethink-server": "localhost:32772",
    "rethink-db": "cloud_mon",
    "rethink-table_low": "cloud_low_utilization",
}


log_config = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s - [%(levelname)s] %(name)s [%(module)s.%(funcName)s:%(lineno)d]: %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
        'info':{
            'format': '%(levelname)s:%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        },
        'debug':{
            'format': '%(asctime)s %(filename)-18s %(levelname)-8s: [ %(funcName)s():%(lineno)s]:  %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        }
    },
    'handlers' : {
        'default': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'debug',
        }
    },
    'loggers': {
        '__main__': { # logging from this module will be logged in VERBOSE level
            'handlers' : ['default'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
    'root': {
        'level': 'INFO',
        'handlers': ['default']
    },
}
