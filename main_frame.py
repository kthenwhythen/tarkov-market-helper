import wx
import mouse
import time
import threading
from scan import Scan
from items import Items
import pandas


class MainFrame(wx.Frame):
    def __init__(self, hash_lang, fps):
        # Set style and options of Frame
        style = (wx.STAY_ON_TOP | wx.FRAME_NO_TASKBAR | wx.SIMPLE_BORDER)
        super().__init__(None, title='Tarkov Market Helper', size=(92, 76), style=style)

        # Style settings
        self.panel = wx.Panel(self)
        self.SetTransparent(220)
        self.SetBackgroundColour('black')

        # Items init
        self.items = Items(hash_lang)

        # Something with item
        self.previous_item_hash = ''
        self.item = pandas.DataFrame()
        self.item_state = 'No item'

        # App settings
        self.update_time = 1 / fps

        # Starting label placeholder
        self.min_price_text = wx.StaticText(self.panel, label='')
        self.slot_price_text = wx.StaticText(self.panel, label='')
        self.trader_price_text = wx.StaticText(self.panel, label='')

        # Init UI
        self.init_ui()

        # Starting thread for positioning frame
        self.thread_is_on = True
        self.turn_thread()

    def turn_thread(self):  # Changing thread bool and then start thread
        self.thread_is_on = not self.thread_is_on

        if self.thread_is_on:
            thread = threading.Thread(target=self.thread_frames)
            thread.start()

    def thread_frames(self):
        while self.thread_is_on:
            self.update_frame()
            time.sleep(self.update_time)
        self.Show(False)

    def update_frame(self):  # Updating frame with position, item hash and UI
        # Update position
        pos_x, pos_y = mouse.get_position()
        wx.CallAfter(self.Move, wx.Point(pos_x + 10, pos_y + 20))

        # Auto scan (hitting performance)
        # if self.mode == 'auto' and self.mode == 'turn':
        self.scan_item()

        # Update item info
        if not self.item.empty and self.item_state == "Item data found" and self.previous_item_hash != self.item[f"Hash {self.items.hash_lang}"].iloc[0]:
            self.previous_item_hash = self.item[f"Hash {self.items.hash_lang}"].iloc[0]
            self.update_ui()
            # print(self.item["Hash EN"].item())
        elif self.item.empty and self.item_state == "Item data not found" \
                and self.previous_item_hash != "":
            self.previous_item_hash = ""
            self.update_ui()

    def init_ui(self):
        hbox = wx.BoxSizer()
        fb = wx.FlexGridSizer(3, 2, 6, 4)

        min_price_title = wx.StaticText(self.panel, size=(12, 16), label='m', style=wx.ALIGN_CENTRE_HORIZONTAL)
        min_price_title.SetForegroundColour((160, 160, 170))

        self.min_price_text = wx.StaticText(self.panel, label=f'₽ N/A')
        self.min_price_text.SetForegroundColour((240, 226, 42))

        slot_price_title = wx.StaticText(self.panel, size=(12, 16), label='s', style=wx.ALIGN_CENTRE_HORIZONTAL)
        slot_price_title.SetForegroundColour((160, 160, 170))

        self.slot_price_text = wx.StaticText(self.panel, label=f'₽ N/A')
        self.slot_price_text.SetForegroundColour((240, 226, 42))

        trader_price_title = wx.StaticText(self.panel, size=(12, 16), label='t', style=wx.ALIGN_CENTRE_HORIZONTAL)
        trader_price_title.SetForegroundColour((160, 160, 170))

        self.trader_price_text = wx.StaticText(self.panel, label=f'₽ N/A')
        self.trader_price_text.SetForegroundColour((240, 226, 42))

        # help_title = wx.StaticText(self.panel, label="(F1)", style=wx.ALIGN_RIGHT)
        # help_title.SetForegroundColour((160, 160, 170))

        fb.AddMany([min_price_title, self.min_price_text,
                    slot_price_title, self.slot_price_text,
                    trader_price_title, self.trader_price_text,
                    ])

        fb.AddGrowableCol(1, 1)

        hbox.Add(fb, proportion=1, flag=wx.EXPAND | wx.ALL, border=6)
        self.panel.SetSizer(hbox)
        self.Layout()

    def update_ui(self):
        if self.item_state == "Item data found":
            self.min_price_text.SetLabel(f"₽{self.item['Lowest price'].iloc[0]}")
            self.slot_price_text.SetLabel(f"₽{self.item['Price per slot'].iloc[0]}")
            self.trader_price_text.SetLabel(f"₽{self.item['Trader price'].iloc[0]}")
        elif self.item_state == "Item data not found":
            self.min_price_text.SetLabel("₽ N/A")
            self.slot_price_text.SetLabel("₽ N/A")
            self.trader_price_text.SetLabel("₽ N/A")

    def scan_item(self):
        try:
            self.item, self.item_state = self.items.find(Scan().item_hash)
        except AttributeError as error:
            print(error)
            self.item, self.item_state = self.items.find('')

        if not self.item.empty and self.item_state == "Item data found" and self.thread_is_on:
            self.Show(True)
        elif self.item.empty and self.item_state == "Item data not found" and self.thread_is_on:
            self.Show(True)
        else:
            self.Show(False)

    def note_item(self):
        print(f'F4: {self.item_state}: {Scan().item_hash}')
