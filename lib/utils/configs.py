import os

class Configs():
    # get defined .env variables

    # MQTT
    MQTT_HOST = os.environ.get("MQTT_HOST", "localhost")
    MQTT_PORT = os.environ.get("MQTT_PORT", 1883)
    MQTT_USERNAME = os.environ.get("MQTT_USERNAME", "admin")
    MQTT_PASSWORD = os.environ.get("MQTT_PASSWORD", "admin")
    MQTT_CLUSTER_URL = os.environ.get("MQTT_CLUSTER_URL", "***")
    MQTT_TOPIC = os.environ.get("MQTT_TOPIC", "default")
    MQTT_CLIENT_ID = os.environ.get("MQTT_CLIENT_ID", "default")
    MQTT_KEEPALIVE = os.environ.get("MQTT_KEEPALIVE", 60)
    MQTT_TLS = os.environ.get("MQTT_TLS", False)
    MQTT_TLS_VERSION = os.environ.get("MQTT_TLS_VERSION", 5)
    MQTT_TLS_CERTFILE = os.environ.get("MQTT_TLS_CERTFILE", None)
    MQTT_TLS_KEYFILE = os.environ.get("MQTT_TLS_KEYFILE", None)
    MQTT_TLS_CA_CERTS = os.environ.get("MQTT_TLS_CA_CERTS", None)
    MQTT_TLS_CIPHERS = os.environ.get("MQTT_TLS_CIPHERS", None)
    MQTT_TLS_CERT_REQS = os.environ.get("MQTT_TLS_CERT_REQS", None)
    MQTT_TLS_INSECURE = os.environ.get("MQTT_TLS_INSECURE", False)
    MQTT_TLS_SESSION = os.environ.get("MQTT_TLS_SESSION", False)

