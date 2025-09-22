#
# MQTT Game Renda OH 
#  for player(02)
#  main function
#  v0.01 (2025/8/2)
#  v0.02 (2025/8/14)
#     Bug fix: Missing argument ui_config in GamePlayer
#  v0.03 (2025/9/14)
#     Added support for dual MQTT brokers: local Mosquitto + AWS IoT Core
#     Connection settings managed via MqttServerConfig dictionary
#  v0.05 2025/9/22
#    Correct CERT file key name in configuration



from player import GamePlayer
from game_agent import GameAgent
from mylib import get_uniq_id

GPIO_SWITCH = 0
GPIO_SPEAKER = 16
GPIO_NEOPIXEL = 17
#NEOPIXEL_LED_SIZE = 24
NEOPIXEL_LED_SIZE = 12

# broker config for local server
BROKER_CONFIG_LOCAL = {
    'broker_endpoint' : '192.168.10.100',
    'broker_port' : 1883,
    'use_TLS': False,
    'TLS_config' : {}
}

# broker config for cloud mqtt server (AWS IoT Core)
BROKER_CONFIG_AWS_IOT_CORE = {
    'broker_endpoint' : 'a3bwzjwa2nkf7t-ats.iot.ap-northeast-1.amazonaws.com',
    'broker_port' : 8883,
    'use_TLS': True,
    'TLS_config' : {
        'client_key_file' : '/cert/private.der.key',
        'client_cert_file' : '/cert/client.der.crt',
        'root_ca_file' : '/cert/AmazonRootCA1.der',
    }
}


def main():

    broker_config = BROKER_CONFIG_AWS_IOT_CORE
    game_agent = GameAgent('player', broker_config)

    player_id = get_uniq_id('pico2w_', length=8)
    player_nick_name = 'player02_5678'
    
    ui_config = {
        'GPIO_SWITCH' : GPIO_SWITCH,
        'GPIO_SPEAKER' : GPIO_SPEAKER,
        'GPIO_NEOPIXEL' : GPIO_NEOPIXEL,
        'NEOPIXEL_LED_SIZE' : NEOPIXEL_LED_SIZE
    }

    game_player = GamePlayer(game_agent, player_id, player_nick_name, ui_config)

    game_player.main_loop()
    
    
main()



#
#
#
