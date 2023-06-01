import pyautogui

OPEN_NOX = "OPEN_NOX"
OPEN_CLASH_ROYALE = "OPEN_CLASH_ROYALE"

def open_emulator(location_handler):
    open_emulator_task = OPEN_NOX
    while True:
        if(open_emulator_task == OPEN_NOX):
            nox_assistant_button = location_handler.get_location("nox_assistant.png")
            if(nox_assistant_button != None):
                open_emulator_task = OPEN_CLASH_ROYALE
                pyautogui.click(nox_assistant_button)
                print("nox assistant opened")

        if(open_emulator_task == OPEN_CLASH_ROYALE):
            clash_royale_button = location_handler.get_location("nox_clash_royale.png")
            if(clash_royale_button != None):
                pyautogui.click(clash_royale_button)
                print("clash royale opened")
                break