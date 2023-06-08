import pyautogui
import win32con
import win32gui
import time
import exit_codes

PERMITTED_TIME_TO_OPEN_CLASH_ROYALE = 60

class EmulatorHandler:

    def __init__(self):
        self.OPEN_NOX = "OPEN_NOX"
        self.OPEN_CLASH_ROYALE = "OPEN_CLASH_ROYALE"

    def open_emulator(self,location_handler):
        print("opening emulator")
        start_time = time.time()
        open_emulator_task = self.OPEN_NOX
        while True:

            if time.time() - start_time > PERMITTED_TIME_TO_OPEN_CLASH_ROYALE:
                return exit_codes.FATAL_ERROR

            if(open_emulator_task == self.OPEN_NOX):
                nox_assistant_button = location_handler.get_location("nox_assistant.png")
                if(nox_assistant_button != None):
                    open_emulator_task = self.OPEN_CLASH_ROYALE
                    pyautogui.click(nox_assistant_button)
                    print("nox assistant opened")

            if(open_emulator_task == self.OPEN_CLASH_ROYALE):
                print("sleeping so we don't make more locate calls than we need to")
                time.sleep(3)
                clash_royale_button = location_handler.get_location("nox_clash_royale.png")
                if(clash_royale_button != None):
                    pyautogui.click(clash_royale_button)
                    print("clash royale opened")
                    return exit_codes.SUCCESS

    #https://stackoverflow.com/questions/59868194/rename-a-window/66141368#66141368
    def __windows_to_close(self,handle, more):
        """private function that will be called on all open windows, and will tell ones related to the emulator to close"""
        title = win32gui.GetWindowText(handle)
        if title.startswith("Nox") or title.startswith("Clash Royale"):
            win32gui.PostMessage(handle,win32con.WM_CLOSE,0,0)
            print("closing: "+title)

    def close_emulator(self):
        """calls the __windows_to_close function on all open windows, selectively closing the ones we need to close"""
        print("closing emulator")
        win32gui.EnumWindows(self.__windows_to_close, None)