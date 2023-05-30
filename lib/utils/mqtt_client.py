import time
import json
from datetime import datetime
from busypie import wait, SECOND

from colorama import Fore, Style
import paho.mqtt.client as paho
import paho.mqtt.subscribeoptions as subscribeoptions
from .configs import Configs

class MQTTBrokerClient:
    def __init__(self, client_id, logger, desk_manager):
        self.logger = logger
        self.desk_manager = desk_manager
        #TODO: CLEAN SESSION: Remove all subscriptions and messages when client disconnects, set True if you want to keep messages and subscriptions
        self.client = paho.Client(client_id=client_id, clean_session=Configs.MQTT_CLEAN_SESSION, userdata=None, protocol=paho.MQTTv31)
        self.client.on_connect = self.on_connect
        # self.client.on_ping_response = self.on_ping_response
        self.client.on_subscribe = self.on_subscribe
        self.client.on_message = self.on_message
        self.client.on_publish = self.on_publish
        self.client.on_log = self.on_log
        self.client.tls_set(ca_certs=None, certfile=None, keyfile=None, cert_reqs=paho.ssl.CERT_REQUIRED, tls_version=paho.ssl.PROTOCOL_TLS, ciphers=None)

        # Flags
        self.client.suback_flag = False
        self.client.connected_flag = False
        self.client.subscribed_topics = []

        self.__connect(Configs.MQTT_USERNAME, Configs.MQTT_PASSWORD, Configs.MQTT_CLUSTER_URL, Configs.MQTT_PORT)


    def __connect(self, username, password, cluster_url, port):
        try:
            self.client.username_pw_set(username, password)
            self.client.connect(cluster_url, port, keepalive=Configs.MQTT_KEEPALIVE)
        except Exception as e:
            raise e

    def on_connect(self, client, userdata, flags, rc):
        """Callback when the device receives a CONNACK response from the MQTT bridge."""

        if rc == 0:
            self.client.connected_flag = True
            self.logger.info(f"Connected to MQTT Broker: {Configs.MQTT_CLUSTER_URL}:{Configs.MQTT_PORT}")
        elif rc == 1:
            self.logger.error("Connection Refused - incorrect protocol version")
        elif rc == 2:
            self.logger.error("Connection Refused - invalid client identifier")
        elif rc == 3:
            self.logger.error("Connection Refused - server unavailable")
        elif rc == 4:
            self.logger.error("Connection Refused - bad user name or password")
        elif rc == 5:
            self.logger.error("Connection Refused - not authorised")
        else:
            self.logger.error(f"Failed to connect, return code {rc}")

    def on_publish(self, client, userdata, mid, properties=None):
        """Callback when the device receives a PUBACK from the MQTT bridge."""
        # self.logger.info("mid: " + str(mid))

    def on_subscribe(self, client, userdata, mid, granted_qos, properties=None):
        """Callback when the device receives a SUBACK from the MQTT bridge."""
        self.client.suback_flag = True

    def on_message(self, client, userdata, msg):
        """Callback when the device receives a message on a subscription."""
        try:
            new_keys = json.loads(msg.payload).keys()
        except json.decoder.JSONDecodeError:
            raise Exception("Payload is not JSON nor JSON-like")
        else:

            if msg.topic not in self.client.subscribed_topics:
                raise Exception("Topic is not subscribed")

            FLOOR, DESK = msg.topic.split("/")
            existing_keys = self.desk_manager.data[FLOOR][DESK].keys()

            if not existing_keys == new_keys:
                raise Exception("Keys are not equal")
            #TODO: check new_values are 0 or 1:
            #check new_values are 0 or 1:

            # MessageLog = {
            #     "TOPIC": msg.topic,
            #     "QOS": msg.qos,
            #     "MESSAGE": msg.payload  # .decode("utf-8")
            # }
            # self.logger.info(MessageLog)
            self.desk_manager.data[FLOOR][DESK] = json.loads(msg.payload)
            self.logger.info(f"Updated {msg.topic} with a received message")

    def on_log(self, client, userdata, level, buf):
        """Callback when the device receives a log from the MQTT bridge."""
        self.logger.info(f"{buf}")

    # def on_ping_response(self, client, userdata, flags, rc):
    #     if rc == paho.MQTT_ERR_SUCCESS:
    #         print("Ping successful")
    #     else:
    #         print("Ping failed")

    def subscribe(self, topic):
        try:
            if isinstance(topic, str):
                self.client.subscribe(topic, qos=0)
                self.wait_for(self.client, "SUBACK")
                self.logger.info(f"Subscribed to topic: {topic}")
                self.client.subscribed_topics.append(topic)
            elif isinstance(topic, list):
                for t in topic:
                    self.client.subscribe(t, qos=0)
                    self.wait_for("SUBACK")
                    self.logger.info(f"Subscribed to topic: {t}")
                    self.client.subscribed_topics.append(t)
            else:
                raise TypeError("Topic must be string or list of strings")
        except Exception as e:
            raise e

    def publish(self, topic, payload):
        # Publish a message to the topic
        result = self.client.publish(topic, payload=payload, qos=0)
        status = result[0]
        if status == 0:
            self.logger.info(f"Send `{payload}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")

    def start(self):
        """
        Loop_start starts a loop in another thread and lets the main thread continue if you need to do other things in the main thread then it is important that it doesn’t end.
        :return:
        :rtype:
        """
        self.client.loop_start()

    def stop(self):
        self.client.disconnect()
        self.client.loop_stop()

    def wait_for(self, msgType, period=0.25):
        if msgType == "CONNACK":
            if self.client.on_connect:
                self.logger.info("Waiting Connack")
                wait().at_most(5, SECOND).poll_interval(0.25, SECOND).until(lambda: self.client.connected_flag)

        if msgType == "DISCONNECT":
            if self.client.on_disconnect:
                while self.client.connected_flag:
                    self.logger.info("waiting disconnect")
                    # self.client.loop()  # check for messages
                    time.sleep(period)

        if msgType == "SUBACK":
            if self.client.on_subscribe:
                self.logger.info("Waiting Suback")
                wait().at_most(3, SECOND).poll_interval(0.25, SECOND).until(lambda: self.client.suback_flag)

        if msgType == "PUBACK":
            if self.client.on_publish:
                print("will wait")
                while not self.client.puback_flag:
                    # self.client.loop()  # check for messages
                    self.logger.info("waiting puback")
                    time.sleep(period)


            # if msgType == "CHECKSUBS":
        #     if check_subs:
        #         print("will wait for all subs")
        #         lcount = 0  # counter to use to exist wait loop
        #         while not check_subs():
        #             self.client.loop()  # check for messages
        #             self.logger.info("waiting for all subscriptions")
        #             time.sleep(period)
        #             if lcount > 20:  # approx 5 seconds
        #                 return False
        #             lcount += 1
            return True