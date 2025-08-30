#
# sample for RP2350
#

import network
import ussl
import socket
from umqtt.simple import MQTTClient

# TLS       
addr_info = socket.getaddrinfo(host, port)[0][-1]
sock = socket.socket()
sock.connect(addr_info)

with open("ca.pem", "rb") as f:
     ca_cert = f.read()
with open("client.pem", "rb") as f:
     client_cert = f.read()
with open("client.key", "rb") as f:
     client_key = f.read()

ssl_sock = ussl.wrap_socket(sock,
                            server_hostname=host,
                            key=client_key,
                            cert=client_cert,
                            ca_certs=ca_cert,
                            cert_reqs=ussl.CERT_REQUIRED)

# MQTT connect
client = MQTTClient(
    client_id = "rp2350-client",
    server = MQTT_BROKER,
    port = 8883,
    ssl_params = {"server_hostname": "mqtt.example.com"},
    sock_factory = ssl_sock,
    ssl = True,
)

# 通信開始
client.connect()
print("MQTT connected with mTLS")

# メッセージ送信
client.publish(b"iot/test", b"Hello from RP2350 with mTLS")

# 終了処理
client.disconnect()
