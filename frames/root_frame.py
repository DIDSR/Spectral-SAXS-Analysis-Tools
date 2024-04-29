import tkinter as tk
from tkinter import ttk
from typing import List, Tuple
from frames import (
    BaseFrame,
    EnergyWindowingFrame,
    ScanReconstructionFrame,
)
from utils.theme import IconName, Icon


class RootFrame(BaseFrame):
    """
        Top-most root frame that holds references to the Tab layout and its two tab frames:
            - EnergyWindowing frame
            - ScanReconstruction frame
    """

    def __init__(self, parent: tk.Tk):
        super().__init__(parent)
        self.parent = parent
        self.setup()

    def title(self) -> str:
        return "Root"

    def setup(self) -> None:
        # Notebook is the Tab widget
        tab_notebook = ttk.Notebook(self.parent, padding=[10, 10, 10, 10])
        tabs: List[Tuple[BaseFrame, IconName]] = [
            (
                # EnergyWindowingFrame(tab_notebook, global_params_frame),
                EnergyWindowingFrame(tab_notebook),
                IconName.ENERGY_WINDOW,
            ),
            (
                # ScanReconstructionFrame(tab_notebook, global_params_frame),
                ScanReconstructionFrame(tab_notebook),
                IconName.SCAN_RECONSTRUCTION,
            ),
        ]
        for tab, icon in tabs:
            img = Icon.load(icon)
            tab.anchor("center")

            tab_notebook.add(tab, text=tab.title(), image=img, compound="left")
            tab.image_ref = img  # without this line, the image won't show. If the image reference is lost, it disappears see: https://stackoverflow.com/questions/41863330/issue-with-button-images-in-ttk-python
        tab_notebook.enable_traversal()
        tab_notebook.grid(row=0, column=0, sticky="nsew")
        tab_notebook.grid_rowconfigure(0, weight=1)
        tab_notebook.grid_columnconfigure(0, weight=1)
