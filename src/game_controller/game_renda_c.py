#
# MQTT Game Renda OH for Game Controller
#
#  main function
#  v0.02  Code optimization: 
#  v0.03 (2025/8/2)
#  v0.04 (2025/8/16)
#    refine comment
#    add ui for controller (M5STACK ATOMS3)
#    if ESP32S3 then change clock to 240MHz
#
#  v0.05 (2025/9/14)
#     Added support for dual MQTT brokers: local Mosquitto + AWS IoT Core
#     Connection settings managed via MqttServerConfig dictionary
#
#  v0.06 (2025/9/21)
#   Bug Fix: Fixed error caused by unset flag for M5STACK detection.
#
#

from controller  import GameController
from game_agent import GameAgent
from mylib import get_uniq_id

# if your controller device is M5STACK ATOMS3,
# then set True else set False for use color display
# https://docs.m5stack.com/ja/core/AtomS3
IS_M5ATOMS3 = True
#IS_M5ATOMS3 = Flase


# broker config for local server
BROKER_CONFIG_LOCAL = {
    'broker_endpoint' : '192.168.10.100',
    'broker_port' : 1883,
    'use_TLS': False,
    'TLS_config' : {}
}


# broker config for cloud mqtt server (AWS IoT Core)
BROKER_CONFIG_AWS_IOT_CORE = {
    'broker_endpoint' : 'a3xxxxx7t-ats.iot.ap-northeast-1.amazonaws.com',
    'broker_port' : 8883,
    'use_TLS': True,
    'TLS_config' : {
        'client_key_file' : '/cert/private.der.key',
        'client_cert_file' : '/cert/client.der.crt',
        'root_ca_file' : '/cert/AmazonRootCA1.der',
    }
}

# Convert the client certificate created in AWS IoT Core from PEM format 
# to DER format using the openssl command.
# command:
#  openssl x509 -in certificate.pem -outform DER -out certificate.der
#
#  The following three types of certificates and the key file, 
#  converted to DER format, are required.
#    (1) Client Certificate
#    (2) Client Private Key
#    (3) Amazon ROOT CA1
#




def main():

    ui = None
    # if contoller is M5ATOMS3, then setup UI
    if IS_M5ATOMS3:
        import os
        if 'M5Stack AtomS3' in os.uname().machine:
           from controller_ui import ControllerUI
           ui = ControllerUI()
           ui.lcd_clear()
           ui.lcd_draw_text(0,0,'MQTT GAME Renda')
           import machine
           machine.freq(240_000_000)
    
    # initialise GameAgent Class
    broker_config = BROKER_CONFIG_AWS_IOT_CORE
    game_agent = GameAgent('controller', broker_config)

    # initialise GameController Class
    game_controller = GameController(game_agent, ui)

    #
    # start Game
    #
    game_controller.main_loop()
    
    
main()



#
#
#