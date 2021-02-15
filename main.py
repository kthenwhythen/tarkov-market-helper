from wx import App
from main_frame import MainFrame
from keyboard import add_hotkey


LANG = 'RU'  # EN, RU
MODE = 'turn'  # auto, turn, btn
HOTKEY = 'F4'  # hotkey for 'turn' and 'btn' mode
FPS = 60

app = App()
main_frame = MainFrame(LANG, MODE, FPS)


# Listener
if MODE == 'turn':
    add_hotkey(HOTKEY, lambda: main_frame.set_thread())
    # add_hotkey('g', lambda: main_frame.update_ui())
elif MODE == 'btn':
    add_hotkey(HOTKEY, lambda: main_frame.update_frame())
    pass

# Debug hotkey
add_hotkey('F2', lambda: main_frame.note_item())

app.MainLoop()
