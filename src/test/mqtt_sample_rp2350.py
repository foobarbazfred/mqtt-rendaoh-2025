################################################ try
#
#   RP2350 sample for AWS IoT  Core
#


import time
import ssl
import json
from umqtt.simple import MQTTClient


MQTT_BROKER = 'a3bwzjwa2nkf7t-ats.iot.ap-northeast-1.amazonaws.com'
MQTT_PORT = 8883             # 8883 : MQTT, encrypted

MQTT_TOPIC = b'test/upy_publish_test'
MQTT_CLIENT_ID = "client_RP_Pico2W_0001"

CLIENT_KEY_FILE = '/cert/private.der.key'
CLIENT_CRT_FILE = 'cert/client.der.crt'
SERVER_CRT_FILE = 'cert/AmazonRootCA1.der.pem'

# read Server side ROOT CA (DER format)
with open(SERVER_CRT_FILE, "rb") as f:
     cadata = f.read()

# parameters for mTLS
ssl_params = {
    "key" : CLIENT_KEY_FILE,
    "cert" : CLIENT_CRT_FILE,
    'cadata' : cadata,
    "cert_reqs" : ssl.CERT_REQUIRED,
    'server_hostname' : MQTT_BROKER,
}
client = MQTTClient( MQTT_CLIENT_ID, MQTT_BROKER, MQTT_PORT, ssl = True, ssl_params = ssl_params )
client.connect()

def on_message(topic, msg):
    print('------------------')
    print("Received: ", topic , '   ' , msg)

client.set_callback(on_message)

TOPIC_ROOT = 'game-renda-0123'
TOPIC_COMMAND_CHANGE_STATE = f'{TOPIC_ROOT}/command/change-state'
client.subscribe(TOPIC_COMMAND_CHANGE_STATE, qos=1)  

while True:
   client.check_msg()
   print('z..')
   time.sleep(0.1)

client.disconnect()




#message = {'client_id': MQTT_CLIENT_ID, 'security settings' : 'with TLS and auth by client crt' }
#payload = json.dumps(message).encode('utf-8')
#print("publish:", payload)
#client.publish(MQTT_TOPIC, payload)
