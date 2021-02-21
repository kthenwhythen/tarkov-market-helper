import wx


class TrayFrame(wx.Frame):
    def __init__(self, position, hotkey_help, hotkey_scan, hotkey_exit):
        """
        TrayFrame is helping user to see the state of the application and view hotkeys
        """
        # Set style and options of Frame
        style = (wx.STAY_ON_TOP | wx.FRAME_NO_TASKBAR | wx.BORDER_NONE)
        super().__init__(None, title='Tarkov Market Helper Tray', size=(50, 20), style=style)
        self.panel = wx.Panel(self)
        self.SetTransparent(220)
        self.SetBackgroundColour('black')

        # Set position on top of display
        self.position = position
        self.set_position(self.position)

        # Taking hotkeys
        self.hotkey_help = hotkey_help
        self.hotkey_scan = hotkey_scan
        self.hotkey_exit = hotkey_exit

        # Mods of app
        self.active = False
        self.help = False

        # Init UI
        self.title = None
        self.hotkeys = None
        self.scan_title = None
        self.scan_text = None
        self.exit_title = None
        self.exit_text = None
        self.m_title = None
        self.m_text = None
        self.s_title = None
        self.s_text = None
        self.t_title = None
        self.t_text = None
        self.init_ui()

        # Show App
        self.Show(True)

    def init_ui(self):
        """
        Init UI when app start
        """
        hbox = wx.BoxSizer()
        fb = wx.FlexGridSizer(7, 2, 4, 6)

        self.title = wx.StaticText(self.panel, label='TMH')
        self.title.SetForegroundColour((160, 160, 170))
        self.hotkeys = wx.StaticText(self.panel, label=f'{self.hotkey_help}')
        self.hotkeys.SetForegroundColour((160, 160, 170))

        self.scan_title = wx.StaticText(self.panel, size=(26, 16), label=f'{self.hotkey_scan}',
                                        style=wx.ALIGN_CENTRE_HORIZONTAL)
        self.scan_title.SetForegroundColour((160, 160, 170))
        self.scan_text = wx.StaticText(self.panel, label='Activate scan')
        self.scan_text.SetForegroundColour((160, 160, 170))

        self.exit_title = wx.StaticText(self.panel, size=(26, 16), label=f'{self.hotkey_exit}',
                                        style=wx.ALIGN_CENTRE_HORIZONTAL)
        self.exit_title.SetForegroundColour((160, 160, 170))
        self.exit_text = wx.StaticText(self.panel, label='Close app')
        self.exit_text.SetForegroundColour((160, 160, 170))

        self.m_title = wx.StaticText(self.panel, size=(26, 16), label='m', style=wx.ALIGN_CENTRE_HORIZONTAL)
        self.m_title.SetForegroundColour((160, 160, 170))
        self.m_text = wx.StaticText(self.panel, label='Avg min price')
        self.m_text.SetForegroundColour((160, 160, 170))

        self.s_title = wx.StaticText(self.panel, size=(26, 16), label='s', style=wx.ALIGN_CENTRE_HORIZONTAL)
        self.s_title.SetForegroundColour((160, 160, 170))
        self.s_text = wx.StaticText(self.panel, label='Per slot price')
        self.s_text.SetForegroundColour((160, 160, 170))

        self.t_title = wx.StaticText(self.panel, size=(26, 16), label='t', style=wx.ALIGN_CENTRE_HORIZONTAL)
        self.t_title.SetForegroundColour((160, 160, 170))
        self.t_text = wx.StaticText(self.panel, label='Trader price')
        self.t_text.SetForegroundColour((160, 160, 170))

        fb.AddMany([self.title, self.hotkeys,
                    self.scan_title, self.scan_text,
                    self.exit_title, self.exit_text,
                    (6, 6), (6, 6),
                    self.m_title, self.m_text,
                    self.s_title, self.s_text,
                    self.t_title, self.t_text
                    ])

        hbox.Add(fb, proportion=1, flag=wx.EXPAND | wx.ALL, border=2)
        self.panel.SetSizer(hbox)
        self.Layout()

    def set_position(self, position):
        """
        Method for set tray_frame position on top
        """
        if position == 'left':
            self.Move(wx.Point(0, 0))

        elif position == 'center':
            self.Move(wx.Point(int((1920 - self.Size.GetWidth()) / 2), 0))

        elif position == 'right':
            self.Move(wx.Point(1920 - self.Size.GetWidth(), 0))

    def turn_active(self):
        """
        On/Off for active scan mode
        """
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
        """
        On/Off for help mode
        """
        self.help = not self.help

        if self.help:
            self.hotkeys.SetForegroundColour((240, 226, 42))
            self.hotkeys.SetLabel('')
            self.SetSize(wx.Size(120, 132))

        else:
            self.hotkeys.SetForegroundColour((160, 160, 170))
            self.hotkeys.SetLabel('')
            self.SetSize(wx.Size(50, 20))

        self.hotkeys.SetLabel(f'{self.hotkey_help}')
        self.set_position(self.position)
