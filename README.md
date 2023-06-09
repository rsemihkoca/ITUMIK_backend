# ITUMIK_backend

## Notes
environment versiyonlama!
configleri mutlaka ayır


![](.README_images/d3ff5e9f.png)

.env instance: 

MQTT_USERNAME = 
MQTT_PASSWORD = 
MQTT_CLUSTER_URL = 
MQTT_PORT = 
MQTT_CLIENT_ID = 
MQTT_KEEPALIVE = 
MQTT_CLEAN_SESSION = 

DB_USERNAME = 
DB_PASSWORD = 
DB_NAME = 
DB_COLLECTION_NAME = 

unit test examples:
Test client creation and requests
https://github.com/mongodb-developer/pymongo-fastapi-crud/blob/main/test_books_crud.py

conda create -n <environment_name> python=3.10 pip --y
conda activate <environment_name>
pip install -r requirements.txt
cd main
python3 main.py


TODO:
* replace error messages with custom ones
* example: raise CustomError(ErrorCodes.mik_ec_001, ErrorMessages.mik_ec_001_MESSAGE, 422, parameters=[Configs.DB_USERNAME, ***REMOVED***])

*Hata alsa da örneğin invalid json dinlemeye devam etmeli benzer yapı on_message'de yapıldı mesaj yanlış olsa da dinlemeye devam ediyor kullanıcıyı bilgilendirmek için log atılıyor