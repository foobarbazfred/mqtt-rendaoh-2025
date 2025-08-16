#  
# controller code for MQTT Renda OH
#
# PC Sample Version
# v0.04  2025/6/28 refactor, 
#    Extracted FSM components into a separate module
# v0.05  2025/6/29 refactor, 
#    refine FSM and push method into FSM
# v0.07  2025/6/29 17:00
#    refine FSM and push method into FSM
# v0.08  2025/6/29 21:00
#    refine timing
# v0.09  2025/6/29 22:00
#    6/29 final
# v0.10  2025/7/1 21:00
#    7/1 final
# v0.11  2025/7/2  22:05
#    Restructured function scopes for improved clarity and logic isolation
# v0.12  2025/7/3
#    Restructured function scopes for improved clarity and logic isolation
# v0.13  2025/7/4
#    Restructured function scopes for improved clarity and logic isolation
# v0.15  2025/7/5
#    Refactored into class form
# v0.16  2025/7/6
#    porting to MicroPython
# v0.17  2025/8/16
#    delete periodically send report
#    add ui for controller (M5STACK ATOMS3)

import time
import json
import random
import gc

class GameController:
 
    def __init__(self, game_agent, ui=None):
        self.session_id = None
        self.game_agent = game_agent
        self.ui = ui
        self.game_agent.set_cb_func_for_controller('STATE_RESULT', self.proc_controller_make_result)

    def main_loop(self):
        while True:
            # in current version, session_is is dummy and not in use
            self.session_id = 'game_session_123_' + random.choice(('a','b','c','x','y','z'))  
            print(f'game start ({self.session_id})')
            if self.ui:
                self.ui.lcd_draw_text(self.ui.UI_TEXT1_POS[0],self.ui.UI_TEXT1_POS[1],'game start')
            self.game_sequence()
            print(f'game finished ({self.session_id})')
            if self.ui:
                self.ui.lcd_draw_text(self.ui.UI_TEXT1_POS[0], self.ui.UI_TEXT1_POS[1],'game fin')


    def game_sequence(self):
    
        current_state = None
        last_state_transfer = 0
        duration = 0
        cmd_seq = 0
    
        # open new game
        current_state, duration = self.game_agent.open_game_by_controller(self.session_id)
        last_state_transfer = time.ticks_ms()

        if self.ui:
            self.ui.lcd_draw_text(self.ui.UI_TEXT2_POS[0], self.ui.UI_TEXT2_POS[1], current_state)

        gc.collect()     # exec garbage collect
        while current_state != 'STATE_CLOSE':
           
            # kick game_agent_task 
            self.game_agent.exec_game_agent_task()
    
            # check trans to next state
            if time.ticks_diff(time.ticks_ms(), last_state_transfer) < duration * 1000:
                pass

            else:
                #  
                # switch to next state
                #  
                next_state = self.game_agent.get_next_state()
                current_state, duration = self.game_agent.change_state_by_controller(next_state)
                if self.ui:
                    self.ui.lcd_draw_text(self.ui.UI_TEXT2_POS[0], self.ui.UI_TEXT2_POS[1], current_state)
                print('wait for ...', duration)
                last_state_transfer =  time.ticks_ms()
                gc.collect()     # exec garbage collect
        

    def proc_controller_make_result(self, game_agent):
        game_member_status = game_agent.get_game_member_status()
        max_click_count = 0
        top_click_user = None
        for id in game_member_status.keys():
             if game_member_status[id]['click_count'] > max_click_count: 
                top_click_user = id
                max_click_count = game_member_status[id]['click_count']
        result = {
            'winner' : top_click_user,
        }
        return result



#
# end of file
#