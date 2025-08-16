#
# MQTT Game Renda OH for Game Controller
#
#  main function
#  v0.02  Code optimization: 
#  v0.03 (2025/8/2)
#  v0.04 (2025/8/16)
#    refine comment
#    add ui for controller (M5STACK ATOMS3)

#
#
from controller  import GameController
from game_agent import GameAgent
from mylib import get_uniq_id

# if your controller device is M5STACK ATOMS3,
# then set True else set False
# https://docs.m5stack.com/ja/core/AtomS3
IS_M5ATOMS3 = True



def main():

    ui = None
    # if contoller is M5ATOMS3, then setup UI
    if IS_M5ATOMS3:
       from controller_ui import ControllerUI
       ui = ControllerUI()
       ui.lcd_clear()
       ui.lcd_draw_text(0,0,'MQTT GAME Renda')
    
    # initialise GameAgent Class
    game_agent = GameAgent('controller')

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