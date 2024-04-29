from binascii import Incomplete
import tkinter as tk
from tkinter.filedialog import askopenfile
from typing import IO, Callable, Dict
from enum import Enum
from pathlib import Path
from models import EnergyWindowingModel
from controllers import GlobalParametersController

"""
Data controller for the Energy Windowing Frame. This file 
"""


class EnergyWindowingController:

    ENERGY_RANGE_MIN, ENERGY_RANGE_MAX = 0, 1000
    ENERGY_RANGE_DEFAULT_MIN, ENERGY_RANGE_DEFAULT_MAX = ENERGY_RANGE_MIN, 100

    class FileOption(Enum):
        BACKGROUND = 1
        SAMPLE = 2

    def __init__(
        self, parent: tk.Tk, global_params_controller: GlobalParametersController
    ):
        self.parent_frame = parent
        self.global_params_controller = global_params_controller
        self._energy_min = tk.IntVar(
            self.parent_frame, self.ENERGY_RANGE_DEFAULT_MIN)
        self._energy_max = tk.IntVar(
            self.parent_frame, self.ENERGY_RANGE_DEFAULT_MAX)
        self._bin_width = tk.IntVar(self.parent_frame, 1)
        self._energy_window_width = tk.IntVar(
            self.parent_frame, self._energy_max.get() - self._energy_min.get()
        )
        self._selected_bg_file_path: str | None = None
        self._selected_sample_file_path: str | None = None
        self._validated_inputs: Dict[str, bool] = {}

    @property
    def energy_range_min(self):
        """The energy range minimum"""
        return self._energy_min

    @energy_range_min.setter
    def energy_range_min(self, value: int):
        self._energy_min.set(value)

    @property
    def energy_range_max(self):
        """The energy range maximum"""
        return self._energy_max

    @energy_range_max.setter
    def energy_range_max(self, value: int):
        self._energy_max.set(value)

    @property
    def bin_width(self):
        """The bin width (keV)"""
        return self._bin_width

    @bin_width.setter
    def bin_width(self, value: int):
        self._bin_width.set(value)

    @property
    def energy_window_width(self):
        """The energy window width (keV)"""
        return self._energy_window_width

    @energy_window_width.setter
    def energy_window_width(self, value: int):
        self._energy_window_width.set(value)

    def are_all_valid(self) -> bool:
        """Whether every input that is meant to be validated is valid"""
        if not self._validated_inputs:
            return False
        are_all_valid = True
        for is_valid in self._validated_inputs.values():
            are_all_valid = are_all_valid and is_valid
        return are_all_valid

    def register_validation(self, entry: str):
        self._validated_inputs[entry] = True

    def register_submit_validation_refresh(self, callback: Callable):
        self._energy_min.trace_add("read", callback)
        self._energy_max.trace_add("read", callback)
        self._bin_width.trace_add("read", callback)
        self._energy_window_width.trace_add("read", callback)

    def validate_energy_min(
        self,
        action: str,
        value: str,
        validation_key: str,
        show_error: Callable[[str], None],
    ) -> bool:
        try:
            intVal = int(value)
            above_floor = intVal >= self.ENERGY_RANGE_MIN
            below_ceil = intVal < self.ENERGY_RANGE_MAX
            less_than_energy_max = intVal < self._energy_max.get()
            is_valid = above_floor and below_ceil and less_than_energy_max
            if is_valid:
                show_error(None)
                self._validated_inputs[validation_key] = True
                return True
            else:
                self._validated_inputs[validation_key] = False
                if not above_floor:
                    show_error(f"Minimum >= {self.ENERGY_RANGE_MIN}")
                if not below_ceil:
                    show_error(f"Maximum < {self.ENERGY_RANGE_MAX}")
                if not less_than_energy_max:
                    show_error("Minimum must be less than Maximum")
                return False
        except ValueError:
            show_error("Invalid value")
            self._validated_inputs[validation_key] = False
            return False
        except tk.TclError:
            show_error("Invalid derived value")
            self._validated_inputs[validation_key] = False
            return False

    def validate_energy_max(
        self,
        action: str,
        value: str,
        validation_key: str,
        show_error: Callable[[str], None],
    ) -> bool:
        try:
            intVal = int(value)
            above_floor = intVal >= self.ENERGY_RANGE_MIN
            below_ceil = intVal < self.ENERGY_RANGE_MAX
            more_than_energy_min = intVal > self._energy_min.get()
            is_valid = above_floor and below_ceil and more_than_energy_min
            if is_valid:
                show_error(None)
                self._validated_inputs[validation_key] = True
                return True
            else:
                self._validated_inputs[validation_key] = False
                if not above_floor:
                    show_error(f"Minimum >= {self.ENERGY_RANGE_MIN}")
                if not below_ceil:
                    show_error(f"Maximum < {self.ENERGY_RANGE_MAX}")
                if not more_than_energy_min:
                    show_error("Maximum must be greater/equal to Minimum")
                return False
        except ValueError:
            show_error("Invalid Value")
            self._validated_inputs[validation_key] = False
            return False
        except tk.TclError:
            show_error("Invalid derived value")
            self._validated_inputs[validation_key] = False
            return False

    def validate_bin_width(
        self,
        action: str,
        value: str,
        validation_key: str,
        show_error: Callable[[str], None],
    ) -> bool:
        try:
            intVal = int(value)
            energy_range = self._energy_max.get() - self._energy_min.get()
            is_valid = energy_range % intVal == 0
            if is_valid:
                self._validated_inputs[validation_key] = True
                show_error(None)
                return True
            else:
                show_error("Bin width not a factor of energy range")
                self._validated_inputs[validation_key] = False
                return False
        except ValueError:
            show_error("Invalid Value")
            self._validated_inputs[validation_key] = False
            return False
        except tk.TclError:
            show_error("Invalid derived value")
            self._validated_inputs[validation_key] = False
            return False

    def validate_energy_window_width(
        self,
        action: str,
        value: str,
        validation_key: str,
        show_error: Callable[[str], None],
    ) -> bool:
        try:
            intVal = int(value)
            energy_range = self._energy_max.get()+1 - self._energy_min.get()
            is_valid = intVal <= energy_range
            if is_valid:
                show_error(None)
                self._validated_inputs[validation_key] = True
                return True
            else:
                show_error(
                    "Energy window must be less than/equal to energy range")
                self._validated_inputs[validation_key] = False
                return False
        except ValueError:
            show_error("Invalid Value")
            self._validated_inputs[validation_key] = False
            return False
        except tk.TclError:
            show_error("Invalid derived value")
            self._validated_inputs[validation_key] = False
            return False

    def browse_file(
        self,
        fileOption: FileOption,
        show_label: Callable[[str], None],
        validation_key: str,
    ):
        file = askopenfile(
            mode="r",
            title="Select a Scan file",
            initialdir="./",
            defaultextension=".hxt",
            filetypes=[
                ("Scan files", ".hxt"),
                ("Text files", ".txt"),
                ("All Files", "*.*"),
            ],
        )
        if file:
            with file:
                file_path = Path(file.name)
                show_label(f"{file_path.stem}{file_path.suffix}")
                self._validated_inputs[validation_key] = True
                if fileOption == self.FileOption.BACKGROUND:
                    self._selected_bg_file_path = str(file_path.absolute())
                elif fileOption == self.FileOption.SAMPLE:
                    self._selected_sample_file_path = str(file_path.absolute())
        else:
            self._validated_inputs[validation_key] = False

    def submit(self):
        print("energy window plotting...")
        print(
            f"Energy: {self._energy_min.get()} - {self._energy_max.get()} \
            \nBin width: {self._bin_width.get()} \
            \nenergy window width: {self._energy_window_width.get()} \
            \nBackground File: {self._selected_bg_file_path} \
            \nSample File: {self._selected_sample_file_path}"
        )
        data = {
            EnergyWindowingModel.Property.ENERGY_RANGE_MIN: self._energy_min.get(),
            EnergyWindowingModel.Property.ENERGY_RANGE_MAX: self._energy_max.get(),
            EnergyWindowingModel.Property.BIN_WIDTH: self._bin_width.get(),
            EnergyWindowingModel.Property.ENERGY_WINDOW_WIDTH: self._energy_window_width.get(),
            EnergyWindowingModel.Property.BACKGROUND_FILE_PATH: self._selected_bg_file_path,
            EnergyWindowingModel.Property.SAMPLE_FILE_PATH: self._selected_sample_file_path,
            EnergyWindowingModel.Property.DETECTOR_DISTANCE_mm: self.global_params_controller.detector_distance.get(),
            EnergyWindowingModel.Property.q_START: self.global_params_controller.q_start.get(),
            EnergyWindowingModel.Property.q_END: self.global_params_controller.q_end.get(),
            EnergyWindowingModel.Property.TRANSMISSION_BEAM_X: self.global_params_controller.transmission_beam_x.get(),
            EnergyWindowingModel.Property.TRANSMISSION_BEAM_Y: self.global_params_controller.transmission_beam_y.get(),
        }
        model = EnergyWindowingModel(data=data)
        model.plot_windowing_figures()
