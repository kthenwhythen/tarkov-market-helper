from wx import App
from tray_frame import TrayFrame
from main_frame2 import MainFrame
from keyboard import add_hotkey


LANG = 'RU'  # EN, RU
MODE = 'turn'  # auto, turn, btn
HOTKEY = 'F4'  # hotkey for 'turn' and 'btn' mode
FPS = 60
TRAY_POSITION = 'right'  # left, center, right


app = App()
main_frame = MainFrame(LANG, MODE, FPS)
tray_frame = TrayFrame()


# Listener
if MODE == 'turn':
    add_hotkey(HOTKEY, lambda: main_frame.turn_thread())
    add_hotkey(HOTKEY, lambda: tray_frame.turn_active())
    # add_hotkey('g', lambda: main_frame.update_ui())
elif MODE == 'btn':
    add_hotkey(HOTKEY, lambda: main_frame.update_frame())


add_hotkey('F1', lambda: tray_frame.turn_help())

# Debug hotkey
add_hotkey('F2', lambda: main_frame.note_item())


add_hotkey('F11', lambda: main_frame.Close())
add_hotkey('F11', lambda: tray_frame.Close())
app.MainLoop()
