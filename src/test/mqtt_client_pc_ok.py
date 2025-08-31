#!/usr/bin/python3

#
# subscribe sample (for PC)
# ans:OK


import os
import time
import datetime
import json
import ssl
import paho.mqtt.client as mqtt
from paho.mqtt.properties import Properties
from paho.mqtt.packettypes import PacketTypes

ENDPOINT = 'a3bwzjwa2nkf7t-ats.iot.ap-northeast-1.amazonaws.com'
PORT = 8883

CA_FILE = './crt/AmazonRootCA1.pem'
CERT_FILE = './crt/16e78b692c53471832783b9a1999c55f21368cda2696c883763db081189abd45-certificate.pem.crt'
KEY_FILE = './crt/16e78b692c53471832783b9a1999c55f21368cda2696c883763db081189abd45-private.pem.key'

TOPIC = "sensor/device01"


is_connected = False

def on_connect(client, userdata, flags, rc, properties=None):
    global is_connected
    if rc == 0:
        print("Connected to AWS IoT Core")
        is_connected = True
        client.subscribe(TOPIC)

        print(f"Subscribed to topic: {TOPIC}")

    else:
        print(f"Failed to connect, return code {rc}")


def on_disconnect(client, userdata, rc, properties=None):
    if rc != 0:
        print("Unexpected disconnection")
    else:
        print("Disconnected from AWS IoT Core")


def on_message(client, userdata, msg):
    global send_time
    try:
        print('-----------------------')
        print(msg.payload)
        #payload = json.loads(msg.payload.decode('utf-8'))
        #print(f"Received message on topic '{msg.topic}':")
        #print(f"Payload: {json.dumps(payload, indent=2)}")
        received_time = datetime.datetime.now()
        elasped_time = received_time - send_time
        print(int(elasped_time.microseconds/1000), 'msec')
    except Exception as e:
        print(f"Error processing message: {e}")


send_time = None
def main():

    global is_connected
    global send_time
    client = mqtt.Client(client_id="myClientID", protocol=mqtt.MQTTv5)
    client.tls_set(
        ca_certs = CA_FILE,
        certfile = CERT_FILE,
        keyfile = KEY_FILE,
        cert_reqs = ssl.CERT_REQUIRED,
        tls_version = ssl.PROTOCOL_TLSv1_2
    )
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message

    client.connect(ENDPOINT, PORT)
    client.loop_start()

    payload = json.dumps({"message": "hello from paho-mqtt"})
    props = Properties(PacketTypes.PUBLISH)
    props.ContentType = "application/json"
    while not is_connected:
        print('z')
        time.sleep(0.5)

    while True:
        send_time = datetime.datetime.now()
        client.publish(TOPIC, payload, qos=0, properties=props)
        time.sleep(1)

    print('closing..')
    time.sleep(1)
    client.loop_stop()
    client.disconnect()

if __name__ == "__main__":
    main()
