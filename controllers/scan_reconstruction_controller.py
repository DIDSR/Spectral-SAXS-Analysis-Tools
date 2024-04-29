import tkinter as tk
import cmath
from tkinter.filedialog import askopenfile, askdirectory
from typing import IO, Callable, Dict, List
from binascii import Incomplete
from pathlib import Path
from models import ScanReconstructionModel
from controllers import GlobalParametersController
from os import listdir, path


"""
Controls the functionality of the buttons and input dialogs for the scan reconstruction frames,
including and validating incoming inputs, sending data to the model, initiating the final analysis. 
"""


class ScanReconstructionController:

    INTEGRAL_Q_MIN, INTEGRAL_Q_MAX, SCAN_WIDTH_MIN = 0.0, 50.0, 1
    INTEGRAL_Q_DEFAULT_START, INTEGRAL_Q_DEFAULT_END, SCAN_WIDTH_DEFAULT = (
        INTEGRAL_Q_MIN,
        30.0,
        SCAN_WIDTH_MIN,
    )
    DEFAULT_SAMPLE_FILE_EXTENSION = ".hxt"
    ENERGY_RANGE_MIN, ENERGY_RANGE_MAX = 0, 1000
    ENERGY_RANGE_DEFAULT_MIN, ENERGY_RANGE_DEFAULT_MAX = ENERGY_RANGE_MIN, 100

    def __init__(
        self, parent: tk.Tk, global_params_controller: GlobalParametersController
    ):
        self.parent_frame = parent
        self.global_params_controller = global_params_controller
        self._energy_min = tk.IntVar(
            self.parent_frame, self.ENERGY_RANGE_DEFAULT_MIN)
        self._energy_max = tk.IntVar(
            self.parent_frame, self.ENERGY_RANGE_DEFAULT_MAX)
        self._integral_q_start = tk.DoubleVar(
            self.parent_frame, self.INTEGRAL_Q_DEFAULT_START
        )
        self._integral_q_end = tk.DoubleVar(
            self.parent_frame, self.INTEGRAL_Q_DEFAULT_END
        )
        self._scan_width = tk.IntVar(
            self.parent_frame, self.SCAN_WIDTH_DEFAULT)
        self._selected_file_extension = tk.StringVar(
            self.parent_frame, self.DEFAULT_SAMPLE_FILE_EXTENSION
        )
        self._selected_bg_file_path: str | None = None
        self._selected_sample_directory: str | None = None
        self._validated_inputs: Dict[str, bool] = {}

    """
    Methods to set and retrieve values from the user input frames
    """
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
    def integral_q_start(self):
        """The q start value"""
        return self._integral_q_start

    @integral_q_start.setter
    def integral_q_start(self, value: float):
        self._integral_q_start.set(value)

    @property
    def integral_q_end(self):
        """The q end value"""
        return self._integral_q_end

    @integral_q_end.setter
    def integral_q_end(self, value: float):
        self._integral_q_end.set(value)

    @property
    def scan_width(self):
        """The scan width"""
        return self._scan_width

    @scan_width.setter
    def scan_width(self, value: int):
        self._scan_width.set(value)

    @property
    def file_extension(self):
        """The selected file extension for the Samples directory"""
        return self._selected_file_extension

    @file_extension.setter
    def file_extension(self, value: str):
        self._selected_file_extension.set(value)

    @property
    def file_extension_options(self) -> List[str]:
        return [".hxt", ".txt"]

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
        self._integral_q_start.trace_add("read", callback)
        self._integral_q_end.trace_add("read", callback)
        self._scan_width.trace_add("read", callback)

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

    def validate_q_start(
        self,
        action: str,
        value: str,
        validation_key: str,
        show_error: Callable[[str], None],
    ) -> bool:
        try:
            floatVal = float(value)
            above_floor = floatVal > self.INTEGRAL_Q_MIN or cmath.isclose(
                floatVal, self.INTEGRAL_Q_MIN
            )
            below_ceil = floatVal < self.INTEGRAL_Q_MAX
            less_than_q_end = floatVal < self._integral_q_end.get()
            is_valid = above_floor and below_ceil and less_than_q_end
            if is_valid:
                show_error(None)
                self._validated_inputs[validation_key] = True
                return True
            else:
                self._validated_inputs[validation_key] = False
                if not above_floor:
                    show_error(f"Minimum >= {self.INTEGRAL_Q_MIN}")
                if not below_ceil:
                    show_error(f"Maximum < {self.INTEGRAL_Q_MAX}")
                if not less_than_q_end:
                    show_error("q start must be less than/equal q end")
                return False
        except ValueError:
            show_error("Invalid value")
            self._validated_inputs[validation_key] = False
            return False
        except tk.TclError:
            show_error("Invalid derived value")
            self._validated_inputs[validation_key] = False
            return False

    def validate_q_end(
        self,
        action: str,
        value: str,
        validation_key: str,
        show_error: Callable[[str], None],
    ) -> bool:
        try:
            floatVal = float(value)
            above_floor = floatVal > self.INTEGRAL_Q_MIN or cmath.isclose(
                floatVal, self.INTEGRAL_Q_MIN
            )
            below_ceil = floatVal < self.INTEGRAL_Q_MAX
            more_than_q_start = floatVal > self._integral_q_start.get()
            is_valid = above_floor and below_ceil and more_than_q_start
            if is_valid:
                show_error(None)
                self._validated_inputs[validation_key] = True
                return True
            else:
                self._validated_inputs[validation_key] = False
                if not above_floor:
                    show_error(f"q Start >= {self.INTEGRAL_Q_MIN}")
                if not below_ceil:
                    show_error(f"q End < {self.INTEGRAL_Q_MAX}")
                if not more_than_q_start:
                    show_error("q end must be more than q start")
                return False
        except ValueError:
            show_error("Invalid value")
            self._validated_inputs[validation_key] = False
            return False
        except tk.TclError:
            show_error("Invalid derived value")
            self._validated_inputs[validation_key] = False
            return False

    def validate_scan_width(
        self,
        action: str,
        value: str,
        validation_key: str,
        show_error: Callable[[str], None],
    ) -> bool:
        try:
            intVal = int(value)
            is_valid = intVal >= 0
            if is_valid:
                show_error(None)
                self._validated_inputs[validation_key] = True
                return True
            else:
                self._validated_inputs[validation_key] = False
                show_error("Scan width cannot be negative")
                return False
        except ValueError:
            show_error("Invalid value")
            self._validated_inputs[validation_key] = False
            return False
        except tk.TclError:
            show_error("Invalid derived value")
            self._validated_inputs[validation_key] = False
            return False

    def browse_bg_file(self, show_label: Callable[[str], None], validation_key: str):
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
                self._selected_bg_file_path = str(file_path.absolute())
        else:
            self._validated_inputs[validation_key] = False

    def browse_sample_directory(
        self, show_label: Callable[[str], None], validation_key: str
    ):
        sample_directory = askdirectory(
            title="Select Samples directory",
            initialdir="./",
        )
        if sample_directory:
            directory_path = Path(sample_directory)
            self._selected_sample_directory = str(directory_path.absolute())
            only_files = [
                file_or_folders
                for file_or_folders in listdir(directory_path.absolute())
                if path.isfile(path.join(directory_path.absolute(), file_or_folders))
            ]
            show_label(
                f"{directory_path.stem} directory; found {len(only_files)}{self._selected_file_extension.get()} files")
            self._validated_inputs[validation_key] = True
        else:
            self._validated_inputs[validation_key] = False

    def submit(self):
        print("scan reconstruction window plotting...")
        print(
            f"q Range: {self._integral_q_start.get()} - {self._integral_q_end.get()} \
            \nEnergy Range: {self._energy_min.get()} - {self._energy_max.get()} \
            \nScan width: {self._scan_width.get()} \
            \nBackground File: {self._selected_bg_file_path} \
            \nSample Directory: {self._selected_sample_directory} \
            \nFile extension: {self._selected_file_extension.get()}"
        )
        data = {
            ScanReconstructionModel.Property.ENERGY_RANGE_MIN: self._energy_min.get(),
            ScanReconstructionModel.Property.ENERGY_RANGE_MAX: self._energy_max.get(),
            ScanReconstructionModel.Property.INTEGRAL_q_START: self._integral_q_start.get(),
            ScanReconstructionModel.Property.INTEGRAL_q_END: self._integral_q_end.get(),
            ScanReconstructionModel.Property.SCAN_WIDTH: self._scan_width.get(),
            ScanReconstructionModel.Property.BACKGROUND_FILE_PATH: self._selected_bg_file_path,
            ScanReconstructionModel.Property.SAMPLE_FILE_PATH: self._selected_sample_directory,
            ScanReconstructionModel.Property.FILE_EXTENSION: self._selected_file_extension.get(),
            ScanReconstructionModel.Property.DETECTOR_DISTANCE_mm: self.global_params_controller.detector_distance.get(),
            ScanReconstructionModel.Property.q_START: self.global_params_controller.q_start.get(),
            ScanReconstructionModel.Property.q_END: self.global_params_controller.q_end.get(),
            ScanReconstructionModel.Property.TRANSMISSION_BEAM_X: self.global_params_controller.transmission_beam_x.get(),
            ScanReconstructionModel.Property.TRANSMISSION_BEAM_Y: self.global_params_controller.transmission_beam_y.get(),
        }

        model = ScanReconstructionModel(data=data)
        model.reconstruct_scan()
