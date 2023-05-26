import time
import paho.mqtt.client as paho
from paho import mqtt
from .configs import Configs


class MQTTBrokerClient:
    def __init__(self, client_id):
        self.client = paho.Client(client_id=client_id, userdata=None, protocol=paho.MQTTv31)
        self.client.on_connect = self.on_connect
        self.client.on_subscribe = self.on_subscribe
        self.client.on_message = self.on_message
        self.client.on_publish = self.on_publish
        self.client.on_log = self.on_log
        self.client.tls_set(ca_certs=None, certfile=None, keyfile=None, cert_reqs=paho.ssl.CERT_REQUIRED, tls_version=paho.ssl.PROTOCOL_TLS, ciphers=None)

        self.__connect(Configs.MQTT_USERNAME, Configs.MQTT_PASSWORD, Configs.MQTT_CLUSTER_URL, Configs.MQTT_PORT)


    def __connect(self, username, password, cluster_url, port):
        try:
            self.client.username_pw_set(username, password)
            self.client.connect(cluster_url, port)
        except Exception as e:
            raise e

    def on_connect(self, client, userdata, flags, rc):

        if rc == 0:
            print("Connection Accepted!")
        elif rc == 1:
            print("Connection Refused - unacceptable protocol version")
        elif rc == 2:
            print("Connection Refused - identifier rejected")
        elif rc == 3:
            print("Connection Refused - server unavailable")
        elif rc == 4:
            print("Connection Refused - bad user name or password")
        elif rc == 5:
            print("Connection Refused - not authorised")
        else:
            print("Failed to connect, return code %d\n", rc)

    def on_publish(self, client, userdata, mid, properties=None):
        print("mid: " + str(mid))

    def on_subscribe(self, client, userdata, mid, granted_qos, properties=None):
        print("Subscribed: " + str(mid) + " " + str(granted_qos))

    def on_message(self, client, userdata, msg):
        print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

    def on_log(self, client, userdata, level, buf):
        print("log: ", buf)

    def subscribe(self, topic):
        self.client.subscribe(topic, qos=0)

    def publish(self, topic, payload):

        msg_count = 0
        while True: # Change this to your requirement
            msg = f"messages: {msg_count}"
            result = self.client.publish(topic, payload=payload, qos=0)
            # result: [0, 1]
            status = result[0]
            if status == 0:
                print(f"Send `{msg}` to topic `{topic}`")
            else:
                print(f"Failed to send message to topic {topic}")
            msg_count += 1

    def start(self):
        self.client.loop_forever()

    def stop(self):
        self.client.disconnect()
        self.client.loop_stop()
