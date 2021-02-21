from wx import App
from keyboard import add_hotkey
from sys import path; path.append('App')
from tray_frame import TrayFrame
from main_frame import MainFrame


# Startup settings
LANG = 'EN'  # EN, RU
HOTKEY_SCAN = 'F4'  # hotkey for turn scan
HOTKEY_HELP = 'F2'  # hotkey for turn help
HOTKEY_EXIT = 'F11'  # hotkey to close app
FPS = 30  # Smooth of frame update
TRAY_POSITION = 'center'  # left, center, right


# Init app
app = App()
main_frame = MainFrame(LANG, FPS)
tray_frame = TrayFrame(TRAY_POSITION, HOTKEY_SCAN, HOTKEY_HELP)


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
