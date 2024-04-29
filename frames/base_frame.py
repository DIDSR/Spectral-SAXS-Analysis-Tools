from tkinter import ttk
from abc import ABCMeta, abstractmethod


class BaseFrame(ttk.Frame, metaclass=ABCMeta):

    @staticmethod
    @abstractmethod
    def title() -> str:
        pass

    @abstractmethod
    def setup() -> None:
        pass
