"""
    CloudWrapper -  Class/Methods to get information and reports overs diferents cloudproviders.
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
from libs.aws_interface import AWSInterface
from libs.db_wrapper import DataStore
from config import main_config
import os
import json

import logging
import logging.config
from config import log_config, main_config
import datetime

logging.config.dictConfig(log_config)
logging.getLogger("cloud_wrapper")


class CloudWrapper:

    def __init__(self, cloud_provider):
        self.cloud_provider = cloud_provider
        logging.debug("The System timezone was setted up to {}".format(os.getenv('TZ')))

    def getInstancePrice(self, instanceID, instanceLocation=None):

        price = None
        if 'aws' in self.cloud_provider:
            aws = AWSInterface()
            price = aws.get_ec2_price(instanceID, instanceLocation)
        return price

    def getInstanceDetails(self, instanceID, instanceLocation=None):
        details = None
        if 'aws' in self.cloud_provider:
            aws = AWSInterface()
            details = aws.get_instance_details(instanceID, instanceLocation)
        return details

    def getSimpleInstanceList(self, state='all', tag_key=None, tag_value=None):
        instances_list = None
        if 'aws' in self.cloud_provider:
            aws = AWSInterface()
            instances_list = aws.get_simple_instances_list(state, tag_key, tag_value)
        return instances_list

    def make_low_utilization(self, tag_key=None, tag_value=None, max_cpu=None, max_mem_available=None, network=None,
                             test_mode=False):
        low_utilizations = None
        ds = DataStore()
        db = "cloud_mon"
        table = None
        if 'aws' in self.cloud_provider:
            table = "aws_low_utilization"
            aws = AWSInterface(test_mode)
            low_utilizations =  aws. get_low_utilization_instances(tag_key=tag_key, tag_value=tag_value,max_cpu=max_cpu,
                                                                   max_mem_available=max_mem_available, network=network)

            ds.save(db, table, low_utilizations)
        if 'googlecloud' in self.cloud_provider:
            low_utilizations = None
            ds.save('gc_low_utilization', low_utilizations)
            pass
        return low_utilizations

    def get_low_utilization_real_time(self, instance_id=None, instance_region=None, tag_value=None, max_cpu=None,
                                      max_mem_available=None, network=None):
        low_utilizations = None
        if 'aws' in self.cloud_provider:
            aws = AWSInterface()
            low_utilizations = aws.get_low_utilization_instances(instance_id, instance_region, tag_key, tag_value,
                                                                 max_cpu, max_mem_available, network)
            return low_utilizations

    def get_low_utilization_from_db(self, instance_id=None, instance_region=None, tag_key=None, tag_value=None):
        ds = DataStore()
        db = "cloud_mon"
        table = "aws_low_utilization"
        low_utilizations = ds.get_low_utilization_db(db, table, instance_id, instance_region, tag_key, tag_value)
        return low_utilizations
