import time
from datetime import datetime

from colorama import Fore, Style
import paho.mqtt.client as paho
from .configs import Configs

count = 0
class MQTTBrokerClient:
    def __init__(self, client_id, logger):
        self.logger = logger
        self.client = paho.Client(client_id=client_id, userdata=None, protocol=paho.MQTTv31)
        self.client.on_connect = self.on_connect
        # self.client.on_ping_response = self.on_ping_response
        self.client.on_subscribe = self.on_subscribe
        self.client.on_message = self.on_message
        self.client.on_publish = self.on_publish
        self.client.on_log = self.on_log
        self.client.tls_set(ca_certs=None, certfile=None, keyfile=None, cert_reqs=paho.ssl.CERT_REQUIRED, tls_version=paho.ssl.PROTOCOL_TLS, ciphers=None)

        self.__connect(Configs.MQTT_USERNAME, Configs.MQTT_PASSWORD, Configs.MQTT_CLUSTER_URL, Configs.MQTT_PORT)


    def __connect(self, username, password, cluster_url, port):
        try:
            self.client.username_pw_set(username, password)
            # Keepalive: 3 sn PNG req gönderir, 3 sn içinde cevap gelmezse bağlantıyı keser
            self.client.connect(cluster_url, port, keepalive=Configs.MQTT_KEEPALIVE)
        except Exception as e:
            raise e

    def on_connect(self, client, userdata, flags, rc):
        global count
        print("count: ", count)
        if rc == 0:
            count+=1
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
        self.logger.info("mid: " + str(mid))

    def on_subscribe(self, client, userdata, mid, granted_qos, properties=None):
        self.logger.info("Subscribed: " + Configs.MQTT_TOPIC)  # str(mid) + " " + str(granted_qos)

    def on_message(self, client, userdata, msg):
        MessageLog = {
            "TOPIC": msg.topic,
            "QOS": msg.qos,
            "MESSAGE": msg.payload.decode("utf-8")
        }
        self.logger.info(MessageLog)

    def on_log(self, client, userdata, level, buf):
        self.logger.info(f"LOG: {buf}")

    # def on_ping_response(self, client, userdata, flags, rc):
    #     if rc == paho.MQTT_ERR_SUCCESS:
    #         print("Ping successful")
    #     else:
    #         print("Ping failed")

    def subscribe(self, topic):
        self.client.subscribe(topic, qos=0)

    def publish(self, topic, payload):
        # Publish a message to the topic TODO:TAMAMLANACAK
        result = self.client.publish(topic, payload=payload, qos=0)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{payload}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")

    def start(self):
        # self.client.loop_forever()
        self.client.loop_start()
        # keep alive süresi içinde pingreq gönderir, pingresp cevabı gelmezse bağlantıyı keser
        # gelen cevap 0 ise bağlantı sağlıklı, rc ile kontrol edilir
        # şimdilik es geçilebilir

        # while True: # rc ?= 0
        #     self.client._send_pingreq()
        #     # Diğer işlemleri burada gerçekleştirin
        #     print(f"{datetime.now()}: {Fore.GREEN} Consumer Health Check: OK{Style.RESET_ALL}")
        #     #self.logger.info(f"datetime.now(): {Fore.GREEN}Health Check: OK{Style.RESET_ALL}")
        #     time.sleep(5)

    def stop(self):
        self.client.disconnect()
        self.client.loop_stop()
