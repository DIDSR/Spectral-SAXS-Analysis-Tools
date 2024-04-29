# -*- coding: utf-8 -*-
"""
@author: Sabri.Amer
"""

import tkinter as tk
from utils import Constants
from utils.theme import get_system_theme, Icon, IconName
from frames import RootFrame
import sv_ttk


class MainWindow:

    MIN_WIDTH, MIN_HEIGHT = 1200, 800

    def __init__(self):
        self.root = tk.Tk()
        self.root.wm_iconphoto(False, Icon.load(IconName.FAVICON))
        self.root.title(Constants.APP_TITLE)
        self.root.minsize(MainWindow.MIN_WIDTH, MainWindow.MIN_HEIGHT)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.anchor("center")
        # sets the Sun Valley theme. theme options are 'dark' and 'light'
        sv_ttk.set_theme(theme=get_system_theme())
        self.init_frame()

    def init_frame(self) -> None:
        root_frame = RootFrame(self.root)
        root_frame.grid(column=0, row=0, sticky="nsew")
        root_frame.grid_rowconfigure(0, weight=1)
        root_frame.grid_columnconfigure(0, weight=1)

    def show(self) -> None:
        self.root.mainloop()
