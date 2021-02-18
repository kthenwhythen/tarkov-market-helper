import wx


class TrayFrame(wx.Frame):
    def __init__(self):

        # Set style and options of Frame
        style = (wx.STAY_ON_TOP | wx.FRAME_NO_TASKBAR | wx.BORDER_NONE)
        super().__init__(None, title='Tarkov Market Helper Tray', size=(76, 20), style=style)

        # Style settings
        self.panel = wx.Panel(self)
        self.SetTransparent(220)
        self.SetBackgroundColour('black')
        self.Move(wx.Point(1844, 0))

        self.active = False
        self.help = False

        hbox = wx.BoxSizer()
        fb = wx.FlexGridSizer(2, 2, 6, 6)

        self.title = wx.StaticText(self.panel, label='TMH')
        self.title.SetForegroundColour((160, 160, 170))

        self.hotkeys = wx.StaticText(self.panel, label='F1-help')
        self.hotkeys.SetForegroundColour((160, 160, 170))

        fb.AddMany([self.title, self.hotkeys])

        hbox.Add(fb, proportion=1, flag=wx.EXPAND | wx.ALL, border=2)
        self.panel.SetSizer(hbox)
        self.Layout()

        # Show App
        self.Show(True)

    def turn_active(self):
        self.active = not self.active
        if self.active:
            self.title.SetForegroundColour((240, 226, 42))
            self.title.SetLabel('')
        else:
            self.title.SetForegroundColour((160, 160, 170))
            self.title.SetLabel('')
        self.title.SetLabel('TMH')
        self.Layout()

    def turn_help(self):
        self.help = not self.help
        if self.help:
            self.hotkeys.SetForegroundColour((240, 226, 42))
            self.hotkeys.SetLabel('')
            self.SetSize(wx.Size(76, 100))
            self.panel_help = wx.Panel(self)
        else:
            self.hotkeys.SetForegroundColour((160, 160, 170))
            self.hotkeys.SetLabel('')
            self.SetSize(wx.Size(76, 20))
        self.hotkeys.SetLabel('F1-help')

    def init_help_ui(self):
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
        pass
