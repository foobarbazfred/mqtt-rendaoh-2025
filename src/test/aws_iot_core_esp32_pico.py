#
# AWS IoT Core (org:sample04.py)
#
# MQTT over TLS with mutual authentication (mTLS) sample.
# Connects to test.mosquitto.org using client certificate authentication,
# publishes a test message, then disconnects.
#

from umqtt.simple import MQTTClient
import ssl
import json

MQTT_BROKER = 'a3xxxxxxxx7t-ats.iot.ap-northeast-1.amazonaws.com'
MQTT_PORT = 8883             # 8883 : MQTT, encrypted

MQTT_TOPIC = b'test/upy_publish_test'
MQTT_CLIENT_ID = "client_ESP32_PICO_001"

CLIENT_KEY_FILE = 'client.key.der'
CLIENT_CRT_FILE = 'client.crt.der'
SERVER_CRT_FILE = 'mosquitto.org.crt.der'

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
message = {'client_id': MQTT_CLIENT_ID, 'security settings' : 'with TLS and auth by client crt' }
payload = json.dumps(message).encode('utf-8')
print("publish:", payload)
client.publish(MQTT_TOPIC, payload)
client.disconnect()










#
# sample by AWS IoT
# https://github.com/aws-samples/aws-iot-core-getting-started-micropython/blob/main/main.py


from umqtt.simple import MQTTClient


MQTT_BROKER = 'a3xxxxxxxx7t-ats.iot.ap-northeast-1.amazonaws.com'
aws_endpoint = MQTT_BROKER
PORT=8883

thing_name = "BlogThing"
client_id = "BlogClient"
private_key = "cert/private.pem.key"
private_cert = "cert/cert.pem.crt"
server_cert = "cert/server.crt"

with open(private_key, 'r') as f:
    key = f.read()

with open(private_cert, 'r') as f:
    cert = f.read()


ssl_params = {"key":key, "cert":cert, "server_side":False}


mqtt = MQTTClient(client_id=client, server=endpoint, port=8883, keepalive=1200, ssl=True, ssl_params=sslp)
mqtt.connect()
client.publish(topic, message)
mqtt.check_msg()






########################## in fail -> OK
# Traceback (most recent call last):
#  File "<stdin>", line 1, in <module>
#  File "umqtt/simple.py", line 112, in connect
#IndexError: bytes index out of range


private_key = "cert/private.key"
client_cert = "cert/client.crt"
server_cert = "cert/server.crt"

from umqtt.simple import MQTTClient

MQTT_BROKER = 'a3xxxxxxxx7t-ats.iot.ap-northeast-1.amazonaws.com'
PORT=8883

with open(private_key, 'r') as f:
    key = f.read()
with open(client_cert, 'r') as f:
    cert = f.read()

with open(server_cert, 'r') as f:
    server_cert = f.read()

ssl_params = {"key":private_key, "cert":client_cert, "cadata" : server_cert, "server_side":False}


CLIENT_ID = "ESP32Pico_001"

mqtt = MQTTClient(client_id=CLIENT_ID, server=MQTT_BROKER, port=8883, keepalive=1200, ssl=True, ssl_params=ssl_params)

mqtt.connect()
client.publish(topic, message)
mqtt.check_msg()
mqtt.disconnect()







https://github.com/aws-samples/aws-iot-core-getting-started-micropython/blob/main/main.py




########################################################## try ng -> OK
# 
# >>> client.connect()
# Traceback (most recent call last):
#   File "<stdin>", line 1, in <module>
#   File "umqtt/simple.py", line 112, in connect
# IndexError: bytes index out of range
#  NG -> OK (after activate CERT)

from umqtt.simple import MQTTClient
import ssl
import json

MQTT_BROKER = 'a3xxxxxxxx7t-ats.iot.ap-northeast-1.amazonaws.com'
MQTT_PORT = 8883             # 8883 : MQTT, encrypted

MQTT_TOPIC = b'test/upy_publish_test'
MQTT_CLIENT_ID = "client_ESP32_PICO_001"

CLIENT_KEY_FILE = '/cert/private.key'
CLIENT_CRT_FILE = '/cert/client.crt'
SERVER_CRT_FILE = 'cert/AmazonRootCA1.pem'

#The certificate is not correctly signed by the trusted CA
#SERVER_CRT_FILE = 'cert/AmazonRootCA3.pem'  

# read Server side ROOT CA (PEM format)
with open(SERVER_CRT_FILE, "r") as f:
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
message = {'client_id': MQTT_CLIENT_ID, 'security settings' : 'with TLS and auth by client crt' }
payload = json.dumps(message).encode('utf-8')
print("publish:", payload)
client.publish(MQTT_TOPIC, payload)
client.disconnect()



########################################################## try / error -> ok
#
#Traceback (most recent call last):
#  File "<stdin>", line 28, in <module>
#  File "umqtt/simple.py", line 112, in connect
#IndexError: bytes index out of range  ---> OK
#

from umqtt.simple import MQTTClient
import ssl
import json

MQTT_BROKER = 'a3xxxxxxxx7t-ats.iot.ap-northeast-1.amazonaws.com'
MQTT_PORT = 8883             # 8883 : MQTT, encrypted

MQTT_TOPIC = b'test/upy_publish_test'
MQTT_CLIENT_ID = "client_ESP32_PICO_001"

CLIENT_KEY_FILE = '/cert/private.der.key'
CLIENT_CRT_FILE = '/cert/client.der.crt'
SERVER_CRT_FILE = 'cert/AmazonRootCA1.der'

# read Server side ROOT CA (PEM format)
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
message = {'client_id': MQTT_CLIENT_ID, 'security settings' : 'with TLS and auth by client crt' }
payload = json.dumps(message).encode('utf-8')
print("publish:", payload)
client.publish(MQTT_TOPIC, payload)
client.disconnect()










############################################ try -> OK
#
#
#
#Traceback (most recent call last):
#  File "<stdin>", line 34, in <module>
#  File "umqtt/simple.py", line 112, in connect
#IndexError: bytes index out of range
#  -->     OK  (activate      )

from umqtt.simple import MQTTClient
import ssl
import json

MQTT_BROKER = 'a3xxxxxxxx7t-ats.iot.ap-northeast-1.amazonaws.com'
MQTT_PORT = 8883             # 8883 : MQTT, encrypted

MQTT_TOPIC = b'test/upy_publish_test'
MQTT_CLIENT_ID = "client_ESP32_PICO_001"

CLIENT_KEY_FILE = '/cert/private.der.key'
CLIENT_CRT_FILE = '/cert/client.der.crt'
SERVER_CRT_FILE = 'cert/AmazonRootCA1.der'

with open(CLIENT_KEY_FILE, 'rb') as f:
    key = f.read()

with open(CLIENT_CRT_FILE, 'rb') as f:
    cert = f.read()

# read Server side ROOT CA (PEM format)
with open(SERVER_CRT_FILE, "rb") as f:
     cadata = f.read()

# parameters for mTLS
ssl_params = {
    "key" : key,
    "cert" : cert,
    'cadata' : cadata,
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




##################################### try -> OK
#
#
# Traceback (most recent call last):
#   File "<stdin>", line 1, in <module>
#   File "umqtt/simple.py", line 112, in connect
# IndexError: bytes index out of range   -> OK!!!
#  i#  -->     OK  (activate      ) j

import tls
from umqtt.simple import MQTTClient

KEY_FILE = 'cert/private.der.key'
CERT_FILE ='cert/client.der.crt'
ROOT_CA_FILE ='cert/AmazonRootCA1.der'

with open(KEY_FILE, 'rb') as f:
    key = f.read()
with open(CERT_FILE, 'rb') as f:
    cert = f.read()
with open(ROOT_CA_FILE, 'rb') as f:
    root_ca = f.read()

client_id = "maqueen01"
endpoint = 'a3xxxxxxxx7t-ats.iot.ap-northeast-1.amazonaws.com'

context = tls.SSLContext(tls.PROTOCOL_TLS_CLIENT)
context.load_cert_chain(cert, key)
context.load_verify_locations(root_ca)
client = MQTTClient(client_id, endpoint, port=8883, keepalive=3600, ssl=context)
client.connect(clean_session=True)
import time
while True:
   client.publish('aa/bb/cc', json.dumps({'aa':'bb'}))
   time.sleep(1)





#
# re check by regacy argument
#
############################################ try -> OK
#
#

from umqtt.simple import MQTTClient
import ssl
import json

MQTT_BROKER = 'a3xxxxxxxx7t-ats.iot.ap-northeast-1.amazonaws.com'
MQTT_PORT = 8883             # 8883 : MQTT, encrypted

MQTT_TOPIC = b'test/upy_publish_test'
MQTT_CLIENT_ID = "client_ESP32_PICO_001"

CLIENT_KEY_FILE = '/cert/private.der.key'
CLIENT_CRT_FILE = '/cert/client.der.crt'
SERVER_CRT_FILE = 'cert/AmazonRootCA1.der'

with open(CLIENT_KEY_FILE, 'rb') as f:
    key = f.read()

with open(CLIENT_CRT_FILE, 'rb') as f:
    cert = f.read()

# read Server side ROOT CA (PEM format)
with open(SERVER_CRT_FILE, "rb") as f:
     cadata = f.read()

# parameters for mTLS
ssl_params = {
    "key" : key,
    "cert" : cert,
    'cadata' : cadata,
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





############################################ try -> OK
#
#

from umqtt.simple import MQTTClient
import ssl
import json

MQTT_BROKER = 'a3xxxxxxxx7t-ats.iot.ap-northeast-1.amazonaws.com'
MQTT_PORT = 8883             # 8883 : MQTT, encrypted

MQTT_TOPIC = b'test/upy_publish_test'
MQTT_CLIENT_ID = "client_ESP32_PICO_001"

CLIENT_KEY_FILE = '/cert/private.der.key'
CLIENT_CRT_FILE = '/cert/client.der.crt'
SERVER_CRT_FILE = 'cert/AmazonRootCA1.der'

# read Server side ROOT CA (PEM format)
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
message = {'client_id': MQTT_CLIENT_ID, 'security settings' : 'with TLS and auth by client crt' }
payload = json.dumps(message).encode('utf-8')
print("publish:", payload)
client.publish(MQTT_TOPIC, payload)
client.disconnect()






############################################ try(pem pk??) -> PEM OK
#
#

from umqtt.simple import MQTTClient
import ssl
import json

MQTT_BROKER = 'a3xxxxxxxx7t-ats.iot.ap-northeast-1.amazonaws.com'
MQTT_PORT = 8883             # 8883 : MQTT, encrypted

MQTT_TOPIC = b'test/upy_publish_test'
MQTT_CLIENT_ID = "client_ESP32_PICO_001"

CLIENT_KEY_FILE = '/cert/private.key'
CLIENT_CRT_FILE = '/cert/client.crt'
SERVER_CRT_FILE = '/cert/AmazonRootCA1.pem'

# read Server side ROOT CA (PEM format)
with open(SERVER_CRT_FILE, "r") as f:
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
message = {'client_id': MQTT_CLIENT_ID, 'security settings' : 'with TLS and auth by client crt (pem format)' }
payload = json.dumps(message).encode('utf-8')
print("publish:", payload)
client.publish(MQTT_TOPIC, payload)
client.disconnect()





#
# OK OK
#

import tls
from umqtt.simple import MQTTClient

KEY_FILE = '/cert/private.der.key'
CERT_FILE ='/cert/client.der.crt'
ROOT_CA_FILE ='/cert/AmazonRootCA1.der'

with open(KEY_FILE, 'rb') as f:
    key = f.read()
with open(CERT_FILE, 'rb') as f:
    cert = f.read()
with open(ROOT_CA_FILE, 'rb') as f:
    root_ca = f.read()

client_id = "esp32-pico01"
endpoint = 'a3xxxxxxxx7t-ats.iot.ap-northeast-1.amazonaws.com'

context = tls.SSLContext(tls.PROTOCOL_TLS_CLIENT)
context.load_cert_chain(cert, key)
context.load_verify_locations(root_ca)
client = MQTTClient(client_id, endpoint, port=8883, keepalive=3600, ssl=context)
client.connect(clean_session=True)
client.publish('aa/bb/cc', json.dumps({'aa':'bb'}))
time.sleep(1)
client.disconnect()


###################################  OK
#
# try -> OK

import tls
import json
from umqtt.simple import MQTTClient

endpoint = 'a3xxxxxxxx7t-ats.iot.ap-northeast-1.amazonaws.com'
client_id = "esp32-pico01"

KEY_FILE = '/cert/private.key'
CERT_FILE ='/cert/client.crt'
ROOT_CA_FILE ='/cert/AmazonRootCA1.pem'

with open(KEY_FILE, 'rb') as f:
    key = f.read()
with open(CERT_FILE, 'rb') as f:
    cert = f.read()
with open(ROOT_CA_FILE, 'rb') as f:
    root_ca = f.read()


context = tls.SSLContext(tls.PROTOCOL_TLS_CLIENT)
context.load_cert_chain(cert, key)
context.load_verify_locations(root_ca)
client = MQTTClient(client_id, endpoint, port=8883, keepalive=3600, ssl=context)
client.connect(clean_session=True)
client.publish('aa/bb/cc', json.dumps({'params':'use pem format'}))
time.sleep(1)
client.disconnect()
