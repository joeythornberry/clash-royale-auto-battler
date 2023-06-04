import pyautogui
import time
import exit_codes


CALIBRATE_AND_GET_TO_SEASONAL_SCREEN = "CALIBRATE_AND_GET_TO_SEASONAL_SCREEN"
SELECT_1V1_BATTLE = "SELECT_1V1_BATTLE"
CONFIRM_1V1_BATTLE = "CONFIRM_1V1_BATTLE"
CALIBRATE_BATTLE = "CALIBRATE_BATTLE"
BATTLE = "BATTLE"
END_BATTLE = "END_BATTLE"

TOLERATED_STARTUP_TIME = 180
TOLERATED_TIME_BETWEEN_BATTLES = 420
TOLERATED_TOTAL_RUN_TIME = 1800

STARTUP_PHASE = "STARTUP_PHASE"
BATTLE_PHASE = "BATTLE_PHASE"


def fight_seasonal_battles(location_handler,api_accesser):

    task = CALIBRATE_AND_GET_TO_SEASONAL_SCREEN
    phase = STARTUP_PHASE

    start_time = time.time()
    time_of_last_successful_action = time.time()

    while True:

        time_since_last_successful_action = time.time() - time_of_last_successful_action
        if phase == STARTUP_PHASE and time_since_last_successful_action >= TOLERATED_STARTUP_TIME:
            print("startup took too long")
            return exit_codes.RELOADABLE_ERROR
        elif phase == BATTLE_PHASE and time_since_last_successful_action >= TOLERATED_TIME_BETWEEN_BATTLES:
            print("starting next battle took too long")
            return exit_codes.RELOADABLE_ERROR
        if time.time() - start_time >= TOLERATED_TOTAL_RUN_TIME:
            print("run took too long")
            return exit_codes.RELOADABLE_ERROR

        if(task == CALIBRATE_AND_GET_TO_SEASONAL_SCREEN):
            print("sleeping so we don't make more locate calls than we need to")
            time.sleep(5)
            #use these two images, one at the top left and one at the bottom right (the seasonal button), to estimate the size of the screen
            upper_left_crown = location_handler.get_location("upper_left_crown.png")
            seasonal_button = location_handler.get_location("seasonal_button.png")
            if(upper_left_crown != None and seasonal_button != None):
                screen_width = seasonal_button.x-upper_left_crown.x
                screen_height = seasonal_button.y-upper_left_crown.y
                screen = (upper_left_crown.x,upper_left_crown.y,screen_width,screen_height)
                print("screen size (very roughly) calculated: "+str(screen))
                #click on the seasonal button
                pyautogui.click(seasonal_button)
                print("opened seasonal screen")
                task = SELECT_1V1_BATTLE
        
        if(task == SELECT_1V1_BATTLE):
            #battle_1v1_button = location_handler.get_location("battle_1v1_button.png",screen)
            battle_1v1_button = location_handler.get_location("battle_1v1_button.png",confidence = 0.98,grayscale = False)
            if(battle_1v1_button != None):
                pyautogui.click(battle_1v1_button)
                print("selected 1v1 battle")
                print("sleeping to give confirm button time to show up")
                time.sleep(1)
                task = CONFIRM_1V1_BATTLE

        if(task == CONFIRM_1V1_BATTLE):
            #confirm_1v1_button = location_handler.get_location("confirm_1v1_button.png",screen)
            confirm_1v1_button = location_handler.get_location("confirm_1v1_button.png")
            if(confirm_1v1_button != None):
                pyautogui.click(confirm_1v1_button)
                print("confirmed 1v1 battle")
                phase = BATTLE_PHASE
                time_of_last_successful_action = time.time()
                task = CALIBRATE_BATTLE

        if(task == CALIBRATE_BATTLE):
            print("sleeping so we don't make more locate calls than we need to")
            time.sleep(2)
            #enemy_tower_healthbar = location_handler.get_location("enemy_tower_healthbar.png",region=screen,confidence=0.8)
            enemy_tower_healthbar = location_handler.get_location("enemy_tower_healthbar.png",confidence=0.8)
            if(enemy_tower_healthbar != None):
                #wait for cards to show up (they don't until a little after enemy tower is visible)
                print("sleeping to wait for cards to show up on screen")
                time.sleep(1.5)
                #calculate a target point just in front of the left tower, so that spells will hit it
                target_pointX = enemy_tower_healthbar.x
                #target_pointY = enemy_tower_healthbar.y + screen_height/8
                target_pointY = enemy_tower_healthbar.y + 900/10

                #the reference images we have of each different elixir cost
                card_elixir_icons = ["two_elixir_card_icon.png","three_elixir_card_icon.png","four_elixir_card_icon.png"]
                card_slots = []
                for card_elixir_icon in card_elixir_icons:
                    card_slots.extend(location_handler.get_multiple_locations(card_elixir_icon))

                #when this changes, we'll know the battle has been ended
                last_battle_time = api_accesser.last_battle_time()
                #we'll use this to find how long the battle took
                start_of_current_battle_time = time.time()
                battle_iterations = 0
                task = BATTLE

        if(task == BATTLE):    
            #just loop through each card and drag it to the target point
            for slot in card_slots:
                pyautogui.moveTo(slot[0],slot[1])
                pyautogui.dragTo(target_pointX,target_pointY,0.5)
            battle_iterations += 1
            #only do this every 5 cycles because it takes a while
            if battle_iterations % 5 == 0:
                #detect if the battle has ended by checking if the time of the last battle is different
                if(last_battle_time != api_accesser.last_battle_time()):
                    print("time of last battle has changed, meaning the current battle has ended")
                    length_of_battle_seconds = round(time.time() - start_of_current_battle_time)
                    api_accesser.add_last_battle_season_tokens_to_total(length_of_battle_seconds)
                    maximum_tokens_reached = api_accesser.maximum_tokens_reached()
                    time_of_last_successful_action = time.time()
                    if(maximum_tokens_reached):
                        print("goal reached")
                        return exit_codes.SUCCESS
                    else:
                        print("goal not yet reached")
                    task = END_BATTLE
                
        if(task == END_BATTLE):
            #end_of_battle_ok = location_handler.get_location("end_of_battle_ok.png",region=screen)
            end_of_battle_ok = location_handler.get_location("end_of_battle_ok.png")
            if(end_of_battle_ok != None):
                pyautogui.click(end_of_battle_ok)
                print("battle ended")
                print("sleeping to wait for loading to finish")
                time.sleep(15)
                task = SELECT_1V1_BATTLE