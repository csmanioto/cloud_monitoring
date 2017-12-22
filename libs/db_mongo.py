import configparser, os, logging
# -----------------------------------------
#  Reading api_config.ini
config_ini = os.getenv('CONFIG')
config = configparser.RawConfigParser()
config.read(config_ini)
monitoring_config = config['monitoring']
mongo_config = config['mongo']


# Setup the log
log_setup = config['log']
logger = logging.getLogger()
formatter = logging.Formatter(fmt=log_setup.get('log_format'), datefmt=log_setup.get('log_datefmt'))
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(log_setup.get('log_level'))
logging.getLogger(__name__)
# -------------------------------------------


from pymongo import MongoClient
from pymongo.errors import PyMongoError


class Mongo(object):
    mongo_db = None
    conn = None

    def __init__(self, mongo_server=None, mongo_port=27017):
        try:
            try:
                if  mongo_server is None:
                    mongo_server = mongo_config.get('server')
                client = MongoClient("mongodb://{}".format(mongo_server))
                self.conn = client
            except Exception as e:
                logging.error("Error to connect MongoDB : {}".format(e))

        except Exception as e:
            logging.error("Erro ao conectar no hostname: {0} - {1}".format(mongo_server, e))

    def save(self, mongo_db, mongo_collection, data):
        try:
            db = self.conn[mongo_db][mongo_collection]
            inserted = db.insert_one(data)
            logging.info("Data has been inserted with success in MongoDB : {0}".format(inserted))
            return inserted

        except PyMongoError as e:
            logging.error("Error on insert data - Mongodb {}".format(e))
            logging.info("I have tried to write this data: {}".format(data))
        finally:
            try:
                self.conn.close()
                logging.debug("Connection with mongo has finished")
                pass
            except Exception as e:
                logging.error("Error to finish MongoDB connection: {}".format(e))
                exit(1)

    def get_low_utilizaion_db(self, mongo_db, mongo_collection,  instance_id=None, instance_region=None, tag_key=None, tag_value=None):
        try:
            db = self.conn[mongo_db][mongo_collection]
            documents = None
            if tag_key is not None and tag_value is not None:
                # documents = db.aggregate({"$match": {"instances.{}".format(tag_key): tag_value}}).sort("_id", -1).limit(1)
                documents = db.find({"instances.{}".format(tag_key): tag_value}, {"instances.$": 1}).sort("_id", -1).limit(1)
                result = [(item) for item in documents]

            else:
                documents = db.find().sort("_id", -1).limit(1)
                result = [(item) for item in documents]

            return result
        except Exception as e:
            logging.error("Error on Mongo get_low_utilizaion_db - {}".format(e))
        finally:
            try:
                self.conn.close()
                logging.debug("Connection with mongo has finished")
                pass
            except Exception as e:
                logging.error("Error to finish MongoDB connection: {}".format(e))
                exit(1)
