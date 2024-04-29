import tkinter as tk
from typing import Dict, Callable
import cmath


class GlobalParametersController:

    DETECTOR_DISTANCE_MIN, DEFAULT_DETECTOR_DISTANCE = 0.0, 100.0
    Q_MIN, Q_MAX = 0.0, 50.0
    TRANS_BEAM_X, TRANS_BEAM_Y = 0, 0
    Q_DEFAULT_START, Q_DEFAULT_END = Q_MIN, 30.0

    def __init__(self, parent: tk.Tk):
        self.parent_frame = parent
        self._detector_distance = tk.DoubleVar(
            self.parent_frame, self.DEFAULT_DETECTOR_DISTANCE
        )
        self._q_start = tk.DoubleVar(self.parent_frame, self.Q_DEFAULT_START)
        self._q_end = tk.DoubleVar(self.parent_frame, self.Q_DEFAULT_END)
        self._transmission_beam_x = tk.IntVar(
            self.parent_frame, self.TRANS_BEAM_X)
        self._transmission_beam_y = tk.IntVar(
            self.parent_frame, self.TRANS_BEAM_Y)
        self._validated_inputs: Dict[str, bool] = {}

    @property
    def detector_distance(self):
        """Sample to detector distance (mm)"""
        return self._detector_distance

    @detector_distance.setter
    def detector_distance(self, value: float):
        self._detector_distance.set(value)

    @property
    def q_start(self):
        """The q start value"""
        return self._q_start

    @q_start.setter
    def q_start(self, value: float):
        self._q_start.set(value)

    @property
    def q_end(self):
        """The q end value"""
        return self._q_end

    @q_end.setter
    def q_end(self, value: float):
        self._q_end.set(value)

    @property
    def transmission_beam_x(self):
        """The Transmission Beam X coordinate"""
        return self._transmission_beam_x

    @transmission_beam_x.setter
    def transmission_beam_x(self, value: int):
        self._transmission_beam_x.set(value)

    @property
    def transmission_beam_y(self):
        """The Transmission Beam Y coordinate"""
        return self._transmission_beam_y

    @transmission_beam_y.setter
    def transmission_beam_y(self, value: int):
        self._transmission_beam_y.set(value)

    def register_validation(self, entry: str):
        self._validated_inputs[entry] = True

    def validate_detector_distance(
        self,
        action: str,
        value: str,
        validation_key: str,
        show_error: Callable[[str], None],
    ) -> bool:
        try:
            floatVal = float(value)
            above_floor = floatVal > self.DETECTOR_DISTANCE_MIN or cmath.isclose(
                floatVal, self.DETECTOR_DISTANCE_MIN
            )
            is_valid = above_floor
            if is_valid:
                show_error(None)
                self._validated_inputs[validation_key] = True
                return True
            else:
                self._validated_inputs[validation_key] = False
                if not above_floor:
                    show_error("Detector distance cannot be negative")
                return False
        except ValueError:
            show_error("Invalid value")
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
            above_floor = floatVal > self.Q_MIN or cmath.isclose(
                floatVal, self.Q_MIN)
            below_ceil = floatVal < self.Q_MAX
            less_than_q_end = floatVal < self._q_end.get()
            is_valid = above_floor and below_ceil and less_than_q_end
            if is_valid:
                show_error(None)
                self._validated_inputs[validation_key] = True
                return True
            else:
                self._validated_inputs[validation_key] = False
                if not above_floor:
                    show_error(f"Minimum >= {self.Q_MIN}")
                if not below_ceil:
                    show_error(f"Maximum < {self.Q_MAX}")
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
            above_floor = floatVal > self.Q_MIN or cmath.isclose(
                floatVal, self.Q_MIN)
            below_ceil = floatVal < self.Q_MAX
            more_than_q_start = floatVal > self._q_start.get()
            is_valid = above_floor and below_ceil and more_than_q_start
            if is_valid:
                show_error(None)
                self._validated_inputs[validation_key] = True
                return True
            else:
                self._validated_inputs[validation_key] = False
                if not above_floor:
                    show_error(f"q Start >= {self.Q_MIN}")
                if not below_ceil:
                    show_error(f"q End < {self.Q_MAX}")
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

    def validate_tranmission_beam_location(
        self,
        action: str,
        value: str,
        validation_key: str,
        show_error: Callable[[str], None],
    ) -> bool:
        try:
            int(value)
            show_error(None)
            self._validated_inputs[validation_key] = True
            return True
        except ValueError:
            show_error("Invalid value")
            self._validated_inputs[validation_key] = False
            return False
        except tk.TclError:
            show_error("Invalid derived value")
            self._validated_inputs[validation_key] = False
            return False
