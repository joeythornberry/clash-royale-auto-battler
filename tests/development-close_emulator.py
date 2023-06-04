import sys
sys.path.insert(0, 'clash_royale_auto_battler/')
import emulator_handler

#closes all emulator stuff (just for development, not used by program)
emulator_handler = emulator_handler.EmulatorHandler()
emulator_handler.close_emulator()