import wx
from mouse import get_position
from time import sleep
from threading import Thread
from pandas import DataFrame
from scan import Scan
from items import Items


class MainFrame(wx.Frame):
    def __init__(self, hash_lang, fps):
        """
        Init of MainFrame that show item price when mouse is pointing on an item

        Arguments:
        hash_lang -- chosen lang of game client
        fps -- how often will be updated MainFrame
        """
        # Set style and options of Frame
        style = (wx.STAY_ON_TOP | wx.FRAME_NO_TASKBAR | wx.SIMPLE_BORDER)
        super().__init__(None, title='Tarkov Market Helper', size=(92, 76), style=style)
        self.panel = wx.Panel(self)
        self.SetTransparent(220)
        self.SetBackgroundColour('black')

        # Items init with chosen lang
        self.items = Items(hash_lang)

        # Remember prev item hash to compare with current item hash (for optimization)
        self.previous_item_hash = ''

        # Starting value for item values
        self.item = DataFrame()
        self.item_state = 'No item'

        # MainFrame update time with fps value that get from settings
        self.update_time = 1 / fps

        # Init UI
        self.min_price_text = None
        self.slot_price_text = None
        self.trader_price_text = None
        self.init_ui()

        # Starting thread for positioning frame
        self.thread_is_on = True
        self.turn_thread()

    def turn_thread(self):
        """
        Changing thread bool and then start thread
        """
        self.thread_is_on = not self.thread_is_on

        if self.thread_is_on:
            thread = Thread(target=self.thread_frames)
            thread.start()

    def thread_frames(self):
        """
        Thread body that looping while is on
        """
        while self.thread_is_on:
            self.update_frame()
            sleep(self.update_time)

        self.Show(False)

    def update_frame(self):
        """
        Update frame with position, item hash and UI
        """
        # Update mouse position
        pos_x, pos_y = get_position()
        wx.CallAfter(self.Move, wx.Point(pos_x + 10, pos_y + 20))

        # Scan item that set item_hash and item_state
        self.scan_item()

        # Update item info in UI
        if not self.item.empty and self.item_state == "Item data found" \
                and self.previous_item_hash != self.item[f"Hash {self.items.hash_lang}"].iloc[0]:
            self.previous_item_hash = self.item[f"Hash {self.items.hash_lang}"].iloc[0]
            self.update_ui()

        elif self.item.empty and self.item_state == "Item data not found" \
                and self.previous_item_hash != "":
            self.previous_item_hash = ""
            self.update_ui()

    def init_ui(self):
        """
        Init UI when app start
        """
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

        fb.AddMany([min_price_title, self.min_price_text,
                    slot_price_title, self.slot_price_text,
                    trader_price_title, self.trader_price_text,
                    ])

        hbox.Add(fb, proportion=1, flag=wx.EXPAND | wx.ALL, border=6)
        self.panel.SetSizer(hbox)
        self.Layout()

    def update_ui(self):
        """
        Update UI when thread looping
        """
        if self.item_state == 'Item data found':
            self.min_price_text.SetLabel(f"₽{self.item['Lowest price'].iloc[0]}")
            self.slot_price_text.SetLabel(f"₽{self.item['Price per slot'].iloc[0]}")
            self.trader_price_text.SetLabel(f"₽{self.item['Trader price'].iloc[0]}")

        elif self.item_state == 'Item data not found':
            self.min_price_text.SetLabel('N/A')
            self.slot_price_text.SetLabel('N/A')
            self.trader_price_text.SetLabel('N/A')

    def scan_item(self):
        """
        Scan item when thread looping and set item_hash, item_state
        """
        try:
            self.item, self.item_state = self.items.find(Scan().item_hash)

        except AttributeError as error:
            print(error)
            self.item, self.item_state = self.items.find('')

        if not self.item.empty and self.item_state == 'Item data found' and self.thread_is_on:
            self.Show(True)

        elif self.item.empty and self.item_state == 'Item data not found' and self.thread_is_on:
            self.Show(True)

        else:
            self.Show(False)

    def note_item(self):
        """
        Used for debug purpose
        """
        print(f'Debug Hash: {self.item_state}: {Scan().item_hash}')
