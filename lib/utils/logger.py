import logging
import datetime
# from elasticsearch import Elasticsearch  # Elasticsearch kullanmak için
from lib.configs.constants import Constants
class CustomLogger:
    def __init__(self, index):
        self.index = index
        self.logger = self._create_logger()

    def _create_logger(self):
        logger = logging.getLogger(self.index)
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)
        return logger

    def log(self, level, message, exc_info=False):
        # log_data = {
        #     Constants.TIMESTAMP: self._get_current_timestamp(),
        #     Constants.LEVEL: level,
        #     Constants.MESSAGE: message,
        #     Constants.INDEX: self.index
        # }
        self.logger.log(logging.getLevelName(level), message, exc_info=exc_info)

    def info(self, message):
        self.log(Constants.INFO, message)

    def debug(self, message):
        self.log(Constants.DEBUG, message)

    def error(self, message):
        self.log(Constants.ERROR, message, exc_info=True)


    # def _save_to_elasticsearch(self, level, message):
    #     doc = {
    #         "timestamp": self._get_current_timestamp(),
    #         "level": logging.getLevelName(level),
    #         "indexname": self.index,
    #         "message": message
    #     }
    #     self.es.index(index="logs", body=doc)  # Elasticsearch indeksini buraya uygun şekilde ayarlayın

    @staticmethod
    def _get_current_timestamp():
        return datetime.datetime.now().isoformat()