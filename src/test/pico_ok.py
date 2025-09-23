############ try
#
#
#

from umqtt.simple import MQTTClient
import ssl
import json

from umqtt.simple import MQTTClient
MQTT_BROKER = 'a3xxxxxxx7t-ats.iot.ap-northeast-1.amazonaws.com'
MQTT_PORT=8883

MQTT_TOPIC = b'test/upy_publish_test'
MQTT_CLIENT_ID = "client_ESP32_PICO_001"

CLIENT_KEY_FILE = '/cert/private.der.key'
CLIENT_CRT_FILE = '/cert/client.der.crt'
SERVER_CRT_FILE = '/cert/AmazonRootCA1.der'

# read Server side ROOT CA (DER format)

#with open(CLIENT_KEY_FILE, 'rb') as f:
#    key = f.read()
#with open(CLIENT_CRT_FILE, 'rb') as f:
#    cert = f.read()
with open(SERVER_CRT_FILE, 'rb') as f:
    server_cert = f.read()


# parameters for mTLS
ssl_params = {
    "key" : CLIENT_KEY_FILE,
    "cert" : CLIENT_CRT_FILE,
    'cadata' : server_cert,
    "cert_reqs" : ssl.CERT_REQUIRED,
    'server_hostname' : MQTT_BROKER,
}
client = MQTTClient( MQTT_CLIENT_ID, MQTT_BROKER, MQTT_PORT, ssl = True, ssl_params = ssl_params )
client.connect()
message = {'client_id': MQTT_CLIENT_ID, 'security settings' : 'with TLS and auth by client crt' }
payload = json.dumps(message).encode('utf-8')
print("publish:", payload)
client.publish(MQTT_TOPIC, payload)
client.disconnect()

