from wx import App
from main_frame import MainFrame

from keyboard import add_hotkey

app = App()
main_frame = MainFrame()

# Listener
# add_hotkey('f', lambda: main_frame.scan_item())
# add_hotkey('g', lambda: main_frame.update_ui())
add_hotkey('F4', lambda: main_frame.note_item())

app.MainLoop()
