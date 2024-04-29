from typing import Literal, Union
import darkdetect
from enum import Enum
from os import path
from PIL import Image, ImageTk


def get_system_theme() -> Union[Literal["dark"], Literal["light"]]:
    return "dark" if darkdetect.isDark() else "light"


# Update this with names of new png-based icon files. Do NOT append the file extension or '-dark' suffix
class IconName(str, Enum):
    ENERGY_WINDOW = "energy-window"
    SCAN_RECONSTRUCTION = "scan-reconstruction"
    FAVICON = "favicon"
    FILE_SEARCH = "file-search"
    FOLDER_SEARCH = "folder-search"


class Icon:
    DEFAULT_SIZE = 24
    __BASE_PATH = "assets"

    @staticmethod
    def load(icon_name: IconName) -> ImageTk.PhotoImage:
        icon = icon_name.value
        if get_system_theme() == "dark" and icon_name != IconName.FAVICON:
            icon += "-dark"
        icon_path = path.join(Icon.__BASE_PATH, f"{icon}.png")
        return ImageTk.PhotoImage(
            Image.open(icon_path).resize(
                (Icon.DEFAULT_SIZE, Icon.DEFAULT_SIZE), Image.Resampling.LANCZOS
            )
        )
