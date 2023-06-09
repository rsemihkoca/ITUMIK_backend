from lib.utils.mongo_client import MongoDBClient
from lib.configs.constants import DBConstants as DBC
from lib.utils.configs import Configs
from pymongo import MongoClient
import logging
logger = logging.getLogger()  # Retrieve the root logger

# Establish a connection to MongoDB
client = MongoClient(Configs.DB_CONNECTION_STRING)
db = client[Configs.DB_NAME]
collection = db[Configs.DB_COLLECTION_NAME]

# def read_document(document_field_name, document_field_value):
#     # Start a session for the read operation
#     with client.start_session() as session:
#         # Start a transaction within the session
#         with session.start_transaction():
#             # Check if the document_field_name exists in the collection
#             if document_field_name in collection.find_one().keys():
#                 # Find the document with the matching field and value
#                 documents = collection.find({document_field_name: document_field_value})
#                 # Return the retrieved documents
#                 return list(documents)
#             else:
#                 raise ValueError(f"{document_field_name} does not exist in the collection.")

def update_document(document_field_name, document_field_value, update_data):
    # Start a session for the update operation
    with client.start_session() as session:
        # Start a transaction within the session
        with session.start_transaction():
            # Check if the document_field_name exists in the collection
            if document_field_name in collection.find_one().keys():
                # Update the document with the specified field and value
                collection.update_one({document_field_name: document_field_value}, {DBC.SET: {DBC.VALUES: update_data}})
            else:
                logger.error(f"{document_field_name} does not exist in the collection.")
                return
