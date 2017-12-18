import rethinkdb as r
from rethinkdb.errors import RqlRuntimeError, RqlDriverError

import requests
import logging
import json
from datetime import datetime
from configparser import ConfigParser

from config import main_config

logging.getLogger(__name__)


class Rethink(object):
    rethink_server = None
    rethink_port = None

    def __init__(self, rethink_server=None, rethink_port=28015):
        try:
            if rethink_server is None:
                rethink_server = main_config["rethink-server"]
          #  if rethink_server.split(':')[1]:
                self.rethink_server = str(rethink_server).split(':')[0]
                self.rethink_port = str(rethink_server).split(':')[1]
        except Exception as e:
            logging.error("Error on init class Rethink {}".format(e))

    def save(self, db, table, data):
        try:
            self.conn = r.connect(host=self.rethink_server, port=self.rethink_port, db=db).repl()
            inserted = r.table(table).insert(json.dumps(data)).run(self.conn)
            logging.debug("Data has been inserted with success in RethinkDB : {0}".format(inserted))
            return (inserted)

        except  (RqlRuntimeError, Exception) as e:
            logging.error("Error on insert data - RethinkDB {}".format(e))
        finally:
            try:
                self.conn.close()
                logging.debug("Connection with RethinkDB has finished")
                pass
            except Exception as e:
                logging.error("Error to finish RethinkDB connection: {}".format(e))
                exit(1)

    def read(self, object):
        pass
