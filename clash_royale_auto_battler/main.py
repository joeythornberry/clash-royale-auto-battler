import private
import emulator_handler
import seasonal_battler
import location_handler
import report_handler
import api_accesser
import time
import exit_codes

#make a file called private.py (it's ignored by git) and make these variables
#the full url of the clash-royale-auto-battler/images folder on your computer
BASE_IMAGE_URL = private.base_image_url
#go to developer.clashroyale.com and make a developer key (you can use https://whatismyipaddress.com/ to find your public IP address)
DEVELOPER_KEY = private.developer_key
#your Clash Royale player id (open the game and click on your name--it will open up a window. under your name in that window will be your player ID)
#use ONLY THE PART AFTER THE HASHTAG (the hashtag is represented by a different value in the url we're going to access)
PLAYER_ID_AFTER_HASHTAG = private.player_id_after_hashtag

location_handler = location_handler.LocationHandler(BASE_IMAGE_URL)
emulator_handler = emulator_handler.EmulatorHandler()
api_accesser = api_accesser.ApiAccesser(DEVELOPER_KEY,PLAYER_ID_AFTER_HASHTAG)
report_handler = report_handler.ReportHandler()
seasonal_battler = seasonal_battler.SeasonalBattler()


start_time_seconds = time.time()

while True:
    api_access,api_access_failure_information = api_accesser.verify_api_is_working()
    if api_access == exit_codes.FATAL_ERROR:
        print("FATAL ERROR: failure to access API")
        print("error information: "+str(api_access_failure_information))
        report_handler.log_error(exit_codes.FATAL_ERROR)
        break
    
    open_clash_royale_result = emulator_handler.open_emulator(location_handler)
    if open_clash_royale_result == exit_codes.FATAL_ERROR:
        exit_code = exit_codes.FATAL_ERROR
        print("failed to open clash royale")
        report_handler.log_error(exit_codes.FATAL_ERROR)
        emulator_handler.close_emulator()
        break
    
    fight_seasonal_battles_result = seasonal_battler.fight_seasonal_battles(location_handler,api_accesser,report_handler)
    match fight_seasonal_battles_result:
        case exit_codes.SUCCESS:
            print("success")
            exit_code = exit_codes.SUCCESS
            emulator_handler.close_emulator()
            break
        case exit_codes.FATAL_ERROR:
            print("fatal error")
            exit_code = exit_codes.FATAL_ERROR
            report_handler.log_error(exit_codes.FATAL_ERROR)
            emulator_handler.close_emulator()
            break
        case exit_codes.RELOADABLE_ERROR:
            location_handler.reset()
            report_handler.log_error(exit_codes.RELOADABLE_ERROR)
            emulator_handler.close_emulator()
            print("sleeping to make sure emulator has enough time to close")
            time.sleep(10)

end_time_seconds = time.time()
total_runtime_seconds = end_time_seconds - start_time_seconds
report_handler.complete_report(total_runtime_seconds,exit_code)
report_handler.save_report_as_sql()
time.sleep(3)
print("done")