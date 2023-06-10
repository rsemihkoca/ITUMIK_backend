from pymongo.mongo_client import MongoClient
from .configs import Configs
from lib.configs.constants import Constants, DBConstants


class MongoDBClient:
    def __init__(self, logger):
        self.logger = logger
        self.client = MongoClient(Configs.DB_CONNECTION_STRING)
        self.db = self.client[Configs.DB_NAME]
        self.collection = self.db[Configs.DB_COLLECTION_NAME]
        self.__connnect()

        self.existing_topics = [str(value) for value in self.collection.distinct(DBConstants.TOPIC)]

    def __connnect(self):
        # Send a ping to confirm a successful connection
        try:

            self.db.command('ping')
            self.logger.info("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            self.logger.error("Unable to connect to MongoDB Atlas Cluster. Check your MongoDB Atlas cluster settings.")
            raise e
