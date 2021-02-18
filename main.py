from wx import App
from tray_frame import TrayFrame
from main_frame import MainFrame
from keyboard import add_hotkey


# Startup settings
LANG = 'RU'  # EN, RU
HOTKEY = 'F4'  # hotkey for turn scan
FPS = 60  # Smooth of frame update
TRAY_POSITION = 'right'  # left, center, right


# Init app
app = App()
main_frame = MainFrame(LANG, FPS)
tray_frame = TrayFrame(TRAY_POSITION, HOTKEY)


# Turn scan
add_hotkey(HOTKEY, lambda: main_frame.turn_thread())
add_hotkey(HOTKEY, lambda: tray_frame.turn_active())


# Turn help
add_hotkey('F1', lambda: tray_frame.turn_help())


# Debug hotkey for view hash
add_hotkey('F2', lambda: main_frame.note_item())


# Close app
add_hotkey('F11', lambda: main_frame.Close())
add_hotkey('F11', lambda: tray_frame.Close())

app.MainLoop()
