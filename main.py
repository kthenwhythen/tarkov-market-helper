# TMH is an in-game assistant for tracking market prices
# https://github.com/null-architect/tarkov_market_helper
# Null-architect


import configparser
from wx import App
from keyboard import add_hotkey
from tray_frame import TrayFrame
from main_frame import MainFrame


# Startup settings
config = configparser.ConfigParser()
config.read('settings.ini')

LANG = config['App settings']['lang']
FPS = int(config['App settings']['fps'])
TRAY_POSITION = config['App settings']['tray_position']

HOTKEY_HELP = config['Hotkey settings']['hotkey_help']
HOTKEY_SCAN = config['Hotkey settings']['hotkey_scan']
HOTKEY_EXIT = config['Hotkey settings']['hotkey_exit']


# Init app
app = App()
main_frame = MainFrame(LANG, FPS)
tray_frame = TrayFrame(TRAY_POSITION, HOTKEY_HELP, HOTKEY_SCAN, HOTKEY_EXIT)


# Turn scan
add_hotkey(HOTKEY_SCAN, lambda: main_frame.turn_thread())
add_hotkey(HOTKEY_SCAN, lambda: tray_frame.turn_active())


# Turn help
add_hotkey(HOTKEY_HELP, lambda: tray_frame.turn_help())


# Debug hotkey for view hash
add_hotkey('F3', lambda: main_frame.note_item())


# Close app
add_hotkey(HOTKEY_EXIT, lambda: main_frame.Close())
add_hotkey(HOTKEY_EXIT, lambda: tray_frame.Close())


app.MainLoop()
