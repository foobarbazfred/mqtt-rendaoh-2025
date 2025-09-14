#
#  GameAgent class 
#  manage State Machine and communicate controller and players
#
# file: ~/lang/py/mqtt/game_rk_game_agent/game_agent.py
#
# v0.07  2025/6/29 17:00
#    create game_agent
# v0.08  2025/6/29 22:00
#    6/29 final
# v0.09  2025/7/1 22:20
#    7/1 final
# v0.10  2025/7/2  22:05
#    Restructured function scopes for improved clarity and logic isolation
# v0.11  2025/7/3 
#    Restructured function scopes for improved clarity and logic isolation
# v0.12  2025/7/4
#    Restructured function scopes for improved clarity and logic isolation
# v0.13  2025/7/5
#    Refactored into class form
#    Moved the state transition table into the GameAgent class for encapsulation
# v0.14  2025/7/6
#    porting to MicroPython
# v0.15  2025/7/16
#    adjust QOS
#    Set QoS to 1 when publishing and subscribing to TOPIC_COMMAND_CHANGE_STATE
#
# v0.16 2025/8/15
#  convert simple version to High Performace System
#  connect local MQTT Broker
#
# v0.17 2025/8/16
#    Refactored algorithm: publish only on click events; 
#       removed periodic state publishing mechanism
#  
# v0.18 2025/9/14
#     Added support for dual MQTT brokers: local Mosquitto + AWS IoT Core
#     Connection settings managed via MqttServerConfig dictionary
#



import sys
import json
import time
from topic_defs import *
from umqtt.simple import MQTTClient
from mylib import get_uniq_id
from mylib import timestamp


#
# MQTT Defs
#
#MQTT_BROKER = 'broker.emqx.io'
MQTT_BROKER = '192.168.10.125'   # local mqtt broker mosquitto
MQTT_PORT = 1883

GAME_DURATION = 10   # Constant defining the duration of a click match
INIT_STATE = 'STATE_OPEN'
PERIODIC_INTERVAL = 500  # Constant defining interval (msec) for periodoc send message


# broker_config = {
#   'broker_endpoint' : '192.168.10.100',
#   'broker_port' : 1883,
#   'use_TLS': True | False,
#   'TLS_config' : {
#       'client_key_file' : 'private.der.key',
#       'client_crt_file' : certificate.der.crt',
#       'ca_file' : 'AmazonRootCA1.der',
#   }
# }



class GameAgent:

    def __init__(self, player_or_controller, broker_config):

        self.current_state = None
        self.session_id = None
        self.is_controller = False
        self.is_player = False
        self.game_member_status = None
        self.result = None
        self.broker_config = broker_config
 
        self.game_member_status = {}
        self.result = {}
        self.current_state = INIT_STATE
        self.client = None
        self.cmd_seq = 0
        # var for periodic send message cycle
        self.last_send_player_status_time = 0
        self.last_send_status_time = 0


        #
        # call back for update click info
        # periodic process
        #
        self.CB_PLAYER_DISP_STATUS = None

        #
        #
        #
        self.STATE_BEHAVIORS = {

            'STATE_OPEN' : {
               'topic' : TOPIC_COMMAND_CHANGE_STATE,
               'payload' : {'state' : 'STATE_OPEN'},
               'player_action' : None,
               'duration' : 3,
               'next_state' : 'STATE_READY',
            },
        
            'STATE_READY' : {
               'topic' : TOPIC_COMMAND_CHANGE_STATE,
               'payload' : {'state' : 'STATE_READY'},
               'player_action' : None,
               'duration' : 3,
               'next_state' : 'STATE_COUNTDOWN_TO_START_3',
            },
        
            'STATE_COUNTDOWN_TO_START_3' : {
               'topic' : TOPIC_COMMAND_CHANGE_STATE,
               'payload' : {'state' : 'STATE_COUNTDOWN_TO_START_3'},
               'player_action' : None,
               'duration' : 1,
               'next_state' : 'STATE_COUNTDOWN_TO_START_2',
            },
        
            'STATE_COUNTDOWN_TO_START_2' : {
               'topic' : TOPIC_COMMAND_CHANGE_STATE,
               'payload' : {'state' : 'STATE_COUNTDOWN_TO_START_2'},
               'player_action' : None,
               'duration' : 1,
               'next_state' : 'STATE_COUNTDOWN_TO_START_1',
            },
        
            'STATE_COUNTDOWN_TO_START_1' : {
               'topic' : TOPIC_COMMAND_CHANGE_STATE,
               'payload' : {'state' : 'STATE_COUNTDOWN_TO_START_1'},
               'player_action' : None,
               'duration' : 1,
               'next_state' : 'STATE_START',
            },
        
            'STATE_START' : {
               'topic' : TOPIC_COMMAND_CHANGE_STATE,
               'payload' : {'state' : 'STATE_START'},
               'player_action' : None,
               'duration' : GAME_DURATION  - 3,    # -3 means countdown
               'next_state' : 'STATE_COUNTDOWN_TO_STOP_3',
            },
        
            'STATE_COUNTDOWN_TO_STOP_3' : {
               'topic' : TOPIC_COMMAND_CHANGE_STATE,
               'payload' : {'state' : 'STATE_COUNTDOWN_TO_STOP_3'},
               'player_action' : None,
               'duration' : 1,
               'next_state' : 'STATE_COUNTDOWN_TO_STOP_2',
            },
        
            'STATE_COUNTDOWN_TO_STOP_2' : {
               'topic' : TOPIC_COMMAND_CHANGE_STATE,
               'payload' : {'state' : 'STATE_COUNTDOWN_TO_STOP_2'},
               'player_action' : None,
               'duration' : 1,
               'next_state' : 'STATE_COUNTDOWN_TO_STOP_1',
            },
        
            'STATE_COUNTDOWN_TO_STOP_1' : {
               'topic' : TOPIC_COMMAND_CHANGE_STATE,
               'payload' : {'state' : 'STATE_COUNTDOWN_TO_STOP_1'},
               'player_action' : None,
               'duration' : 1,
               'next_state' : 'STATE_STOP',
            },
        
            'STATE_STOP' : {
               'topic' : TOPIC_COMMAND_CHANGE_STATE,
               'payload' : {'state' : 'STATE_STOP'},
               'player_action' : None,
               'duration' : 3,          # wait for collect player's status
               'next_state' : 'STATE_RESULT',
            },
        
            'STATE_RESULT' : {
               'topic' : TOPIC_COMMAND_CHANGE_STATE,
               'payload' : { 'state' : 'STATE_RESULT' , 
                             'game_member_status' : None,   # set in controller_action
                                                            # value in  _change_state_for_controller(next_state):
                             'result' : None,               # set in xxxxxx
                           },
               'player_action' : None,
               'controller_action' : None,
               'duration' : 5,
               'next_state' : 'STATE_CLOSE',
            },
        
            'STATE_CLOSE' : {
               'topic' : TOPIC_COMMAND_CHANGE_STATE,
               'payload' : {'state' : 'STATE_CLOSE'},
               'player_action' : None,
               'duration' : 0,
               'next_state' : None
            },
        }
        
        print('__init__')

        if player_or_controller == 'controller':
            self.is_controller = True
        elif player_or_controller == 'player':
            self.is_player = True
        #elif player_or_controller == 'player_and_controller'  or player_or_controller == 'controller_and_player':  
        #    self.is_player = True
        #    self.is_controller = True
        else:
            print('Error in game_agent::init(), unkowon type', player_or_controller)
            return None
        self._MQTT_connect()

    def set_cb_func_for_controller(self, cb_name, func):
        if cb_name in self.STATE_BEHAVIORS:
            self.STATE_BEHAVIORS[cb_name]['controller_action'] = func
        else:
            print('Error in set_cb_func')
            print('unknown state name', cb_name)

    def set_cb_func_for_player(self, cb_name, func):
        if cb_name in self.STATE_BEHAVIORS:
            self.STATE_BEHAVIORS[cb_name]['player_action'] = func
        elif  cb_name == 'CB_PLAYER_DISP_STATUS':
            self.CB_PLAYER_DISP_STATUS = func
        else:
            print('Error in set_cb_func')
            print('unknown cb_name', cb_name)
    
    def get_current_state(self):
        return self.current_state
    
    def get_next_state(self, state = None):
        if state is None:
            state = self.current_state
        return self.STATE_BEHAVIORS[state]['next_state']
    
    def get_duration_to_transition(self, state):
        return STATE_BEHAVIORS[state]['duration']
    
    def get_game_member_status(self):
        return self.game_member_status

    def get_result(self):
        return self.result
    
    # publish request from GamePlayer
    # if button is clicked
    def publish_click_event(self, payload):
        topic = TOPIC_PLAYER_CLICK_EVENT
        payload['session_id'] = self.session_id
        print('send(p->c): ' , topic, payload)
        self.client.publish(topic, json.dumps(payload))

    # publish request from GamePlayer
    # to publish status report (n of click)
    def publish_players_status(self, payload):
        topic = TOPIC_PLAYER_REPORT
        payload['session_id'] = self.session_id
        print('send(p->c): ' , topic, payload)
        self.client.publish(topic, json.dumps(payload))

    #
    #
    #
    #
    
    def proc_game_agent_open(self):
        print('open')
        self.game_member_status = {}
        self.result = {}
        self.cmd_seq = 0
    
    # 
    #  ** game_agent as controller **
    #
    # to start game, called from controller
    #
    def open_game_by_controller(self, session_id):             
        self.session_id = session_id
        return self.change_state_by_controller('STATE_OPEN')
    
    def _cbm_store_result(self, topic, payload):
    
        print('cbm_store_result------------------------------------------')
        if self.is_controller is False:
            payload_str = payload.decode('utf-8')
            payload_dic = json.loads(payload_str)
            self.result = payload_dic['result']
            self.game_member_status = payload_dic['game_member_status']
    
    def _cbm_store_session_id(self, topic, payload):

        print('cbm_store_session_id------------------------------------------')
        if self.is_controller is False:
            payload_str = payload.decode('utf-8')
            payload_dic = json.loads(payload_str)
            self.session_id = payload_dic['session_id']
    
    # 
    #  ** game_agent as player **
    # 
    # function: change stete by message
    # return current_state
    #
    def _cbm_change_state_by_message(self, topic, payload):

        print('cs_b_msg')
        topic_str = topic.decode('utf-8')
        if topic_str != TOPIC_COMMAND_CHANGE_STATE:
            print('Error in change state by message')
            print('not collect topic', topic_str)
        payload_str = payload.decode('utf-8')
        payload_dic = json.loads(payload_str)
        state = payload_dic['state']
        if state == 'STATE_OPEN': 
            if self.is_controller is False:   
                self._cbm_store_session_id(topic, payload)
        elif state == 'STATE_RESULT': 
            if self.is_controller is False:
                self._cbm_store_result(topic, payload)
        if state in self.STATE_BEHAVIORS:
            self._exec_player_action(state) 
            self.current_state = state
        else:
            print('Error ! no match next_state in STATE_BEHAVIORS', state)
    
        return self.current_state
    
    
    #
    # change state function
    # flow: controller -> MQTT -> player
    # return value:
    #    current_state:  current state name
    #    duration:  (wait time until transfer to next state)
    #
    def change_state_by_controller(self, state):
    
        agent_ret_val = None
        cont_ret_val = None
    
        if not state in self.STATE_BEHAVIORS:
            print('Error ! no match next_state in STATE_BEHAVIORS', state)
            return (self.current_state, 0)
        else:
            if state == 'STATE_OPEN':
                 self.proc_game_agent_open()
            cont_ret_val = self._exec_controller_action(state)
            #if self.is_player:
            #     self._exec_player_action(state)
    
            print(f'--- state transfer ->({state}) --')
            topic = self.STATE_BEHAVIORS[state]['topic']
            payload = self.STATE_BEHAVIORS[state]['payload']
            duration = self.STATE_BEHAVIORS[state]['duration']
            self.cmd_seq += 1
            payload['session_id'] = self.session_id
            payload['cmd_seq'] = self.cmd_seq
            payload['time_stamp'] = timestamp()
            payload['game_member_status'] = self.game_member_status
            if state == 'STATE_RESULT':
                payload['result'] = cont_ret_val
            print('publish:' , topic, payload)
            self.client.publish(topic, json.dumps(payload), qos=1)
            self.current_state = state
            return  self.current_state , duration
    
    def _exec_controller_action(self, state):
        val = None
        if 'controller_action' in self.STATE_BEHAVIORS[state]:
            func = self.STATE_BEHAVIORS[state]['controller_action']
            if func is not None:
                val = func(self)
        return val

    def _exec_player_action(self, state):
        val = None
        if 'player_action' in self.STATE_BEHAVIORS[state]:
            func = self.STATE_BEHAVIORS[state]['player_action']
            if func is None:
                print('not defined function, skip', state)
                val = None
            else:
                 val = func(self)
        return val
    
    
    #
    #   periodocally publish message
    #
    #
    #    { <player_id> : { 'click_count' : 123  }, ... ,}
    #  
    #
    
    def exec_game_agent_task(self):
        self.client.check_msg()
        if self.is_controller:
            self._send_to_player_game_member_status()
        else:
            pass      # nothing to do
    
    
    #   publish click summary  from controller to player via game_agent 
    #   controller -----> game_agent  --->  player
    #
    #  publish every 0.5sec
    
    def _send_to_player_game_member_status(self):
    
        if self.current_state in ('STATE_OPEN', 'STATE_READY', 'STATE_COUNTDOWN_TO_START_3', 'STATE_COUNTDOWN_TO_START_2', 'STATE_COUNTDOWN_TO_START_1', 'STATE_RESULT', 'STATE_CLOSE'):
            pass
        else:
            if time.ticks_diff(time.ticks_ms(), self.last_send_status_time) < PERIODIC_INTERVAL:
                pass
            else: 
                topic = TOPIC_GAME_SUMMARY
                payload = {
                    'session_id' : self.session_id,
                    'time_stamp' : timestamp(),
                    'game_member_status' : self.game_member_status,
                }
                print('send to players, game member status')
                print(topic, payload)
                self.client.publish(topic, json.dumps(payload))
                self.last_send_status_time = time.ticks_ms()
    
    
    #
    #  receive message from player (click event)
    #
    #  player -> controller via game_agent
    #
    def _cbm_receive_from_player_player_click_event(self, topic, payload):
        payload_str = payload.decode('utf-8')
        payload_dic = json.loads(payload_str)
        player_id = payload_dic['player_id']
        if player_id in self.game_member_status:
            self.game_member_status[player_id]['click_count'] = payload_dic['click_count']
            self.game_member_status[player_id]['time_stamp'] = payload_dic['time_stamp']
        else:
            self.game_member_status[player_id] = payload_dic

    #
    #  receive message from player  (status report)
    #
    #  player -> controller via game_agent 
    #
    def _cbm_receive_from_player_player_status(self, topic, payload):
        payload_str = payload.decode('utf-8')
        payload_dic = json.loads(payload_str)
        player_id = payload_dic['player_id']
        if player_id in self.game_member_status:
            self.game_member_status[player_id]['click_count'] = payload_dic['click_count']
            self.game_member_status[player_id]['time_stamp'] = payload_dic['time_stamp']
        else:
            self.game_member_status[player_id] = payload_dic
    
    #
    # 
    # received  message (game summary ) from  controller via game_agent
    #   game_agent w/controller --->  game_agent w/player
    #
    def _cbm_receive_from_controller_game_member_status(self, topic, payload):
        payload_str = payload.decode('utf-8')
        payload_dic = json.loads(payload_str)
        self.game_member_status = payload_dic['game_member_status']
        func = self.CB_PLAYER_DISP_STATUS
        if func is None:
            print('error! cb func is None==============================')
        else:
            print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
            func(self.game_member_status)

    #
    # MQTT Handlers
    #
    
    def on_message(self, topic, msg):

        payload = msg
        print('------------------')
        print("Received: ", topic , '   ' , payload)
        topic_str = topic.decode('utf-8')
        payload_str = payload.decode('utf-8')
        payload_dic = json.loads(payload_str)
        if self.is_controller:
            if topic_str == TOPIC_PLAYER_CLICK_EVENT:
                # update player state
                self._cbm_receive_from_player_player_click_event(topic, payload)
            elif topic_str == TOPIC_PLAYER_REPORT:
                # update player state
                self._cbm_receive_from_player_player_status(topic, payload)
            else:
                print('Error!! unknown topic(L479)', topic_str)
        else:
            if 'player' in topic_str:
                pass  # skip if plyer in topic (send by me)
            elif topic_str == TOPIC_COMMAND_CHANGE_STATE:
                self.current_state = self._cbm_change_state_by_message(topic, payload)
            elif topic_str == TOPIC_GAME_SUMMARY:
                self._cbm_receive_from_controller_game_member_status(topic, payload)
            else:
                print('Error unkown topic(L488)', topic_str)
            
    def _MQTT_connect(self):
        
        platform = sys.platform
        mqtt_client_id = get_uniq_id(f'{platform}_', length=8)
        broker = self.broker_config['broker_endpoint']
        port = self.broker_config['broker_port']

        if self.broker_config['use_TLS'] is False:
            # local MQTT Broker (e.g. mosquitto local broker)
            self.client = MQTTClient(mqtt_client_id, broker, port)

        else:
            # import for ssl constants
            import ssl

            # cloud MQTT Broker (e.g. AWS IoT Core (require mTLS))
            ca_file = self.broker_config['TLS_config']['root_ca_file']

            # read Server side ROOT CA (DER format)
            with open(ca_file, "rb") as f:
                cadata = f.read()

            # parameters for mTLS
            ssl_params = {
                "key" : self.broker_config['TLS_config']['client_key_file'],
                "cert" : self.broker_config['TLS_config']['client_cert_file'],
                'cadata' : cadata,
                "cert_reqs" : ssl.CERT_REQUIRED,
                'server_hostname' : broker,
            }
            self.client = MQTTClient(mqtt_client_id, broker, port, ssl = True, ssl_params = ssl_params )

        self.client.set_callback(self.on_message)
        self.client.connect()
        if self.is_controller:
            print('subscribe', f"{TOPIC_ROOT}/player/#")
            self.client.subscribe(f"{TOPIC_ROOT}/player/#")
        else:
            print('subscribe', TOPIC_COMMAND_CHANGE_STATE)  
            print('subscribe', TOPIC_GAME_SUMMARY)
            self.client.subscribe(TOPIC_COMMAND_CHANGE_STATE, qos=1)  
            self.client.subscribe(TOPIC_GAME_SUMMARY)
        
        
#
# end of file
#


