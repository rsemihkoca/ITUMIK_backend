import time
import paho.mqtt.client as paho
from paho import mqtt
from .configs import Configs


class MQTTBrokerClient:
    def __init__(self, username, password, cluster_url, port):
        self.client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)
        self.client.on_connect = self.on_connect
        self.client.on_subscribe = self.on_subscribe
        self.client.on_message = self.on_message
        self.client.on_publish = self.on_publish

        self.client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
        self.client.username_pw_set(username, password)
        self.client.connect(cluster_url, port)

    def on_connect(self, client, userdata, flags, rc, properties=None):
        print("CONNACK received with code %s." % rc)

    def on_publish(self, client, userdata, mid, properties=None):
        print("mid: " + str(mid))

    def on_subscribe(self, client, userdata, mid, granted_qos, properties=None):
        print("Subscribed: " + str(mid) + " " + str(granted_qos))

    def on_message(self, client, userdata, msg):
        print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

    def subscribe(self, topic):
        self.client.subscribe(topic, qos=1)

    def publish(self, topic, payload):
        self.client.publish(topic, payload=payload, qos=1)

    def start(self):
        self.client.loop_forever()


