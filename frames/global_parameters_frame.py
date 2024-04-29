import tkinter as tk
from tkinter import ttk
from frames import BaseFrame
from controllers import GlobalParametersController
from utils import WidgetUtils
"""
The file that handles the visual elements of the app for the experimental parameters
"""


class GlobalParametersFrame(BaseFrame):

    def __init__(self, parent: tk.Tk):
        super().__init__(parent)
        self.parent = parent
        self._controller = GlobalParametersController(self.parent)
        self.setup()

    @property
    def controller(self):
        return self._controller

    def title(self) -> str:
        return "Experimental Parameters"

    def setup(self) -> None:
        frame = self.setup_params_frame()
        self.setup_detector_distance(frame)
        self.setup_q_range(frame)
        self.setup_transmission_beam_location(frame)

    def setup_params_frame(self):
        params_section = ttk.Labelframe(self, text=self.title())
        params_section.grid(row=0, column=0,
                            ipadx=20, ipady=20, pady=10)
        params_section.anchor("center")
        return params_section

    def setup_detector_distance(self, frame: tk.LabelFrame):
        # Detector distance label
        detector_distance_label = ttk.Label(
            frame, text="Sample to detector distance (mm)"
        )
        detector_distance_label.grid(
            row=0, column=0, sticky="w", pady=10, padx=10)

        # Detector distance error label
        detector_distance_error_label = ttk.Label(frame, foreground="tomato")
        detector_distance_error_label.grid(
            row=1, column=0, sticky="w", padx=10)

        detector_distance_key = "detector_distance"
        self._controller.register_validation(detector_distance_key)

        # Detector distance entry
        detector_distance_entry = ttk.Entry(
            frame,
            textvariable=self._controller.detector_distance,
            validate="focus",
            width=6,
            validatecommand=(
                frame.register(
                    WidgetUtils.show_error_message(
                        detector_distance_error_label,
                        detector_distance_key,
                        self._controller.validate_detector_distance,
                    )
                ),
                "%d",
                "%P",
            ),
        )
        detector_distance_entry.grid(row=0, column=3, sticky="e", pady=10)

    def setup_q_range(self, frame: tk.LabelFrame):
        # q Range label
        q_range_label = ttk.Label(frame, text="q Range (nm\u207b\u00B9)")
        q_range_label.grid(row=2, column=0, sticky="w", pady=10, padx=10)

        # q Range Error label
        q_range_error_label = ttk.Label(frame, foreground="tomato")
        q_range_error_label.grid(row=3, column=0, sticky="w", padx=10)

        q_start_key = "q_start"
        self._controller.register_validation(q_start_key)

        # q Range Start entry
        q_range_start_entry = ttk.Entry(
            frame,
            width=5,
            textvariable=self._controller.q_start,
            validate="focus",
            validatecommand=(
                frame.register(
                    WidgetUtils.show_error_message(
                        q_range_error_label,
                        q_start_key,
                        self._controller.validate_q_start,
                    )
                ),
                "%d",
                "%P",
            ),
        )
        q_range_start_entry.grid(row=2, column=1, sticky="e", pady=10)

        q_range_separator_label = ttk.Label(frame, text="to")
        q_range_separator_label.grid(
            row=2, column=2, sticky="e", pady=10, padx=10)

        q_end_key = "q_end"
        self._controller.register_validation(q_end_key)
        # q Range End Entry
        q_range_end_entry = ttk.Entry(
            frame,
            width=5,
            textvariable=self._controller.q_end,
            validate="focus",
            validatecommand=(
                frame.register(
                    WidgetUtils.show_error_message(
                        q_range_error_label, q_end_key, self._controller.validate_q_end
                    )
                ),
                "%d",
                "%P",
            ),
        )
        q_range_end_entry.grid(row=2, column=3, sticky="e", pady=10)

    def setup_transmission_beam_location(self, frame: tk.LabelFrame):
        # Transmission beam location label
        trans_beam_location_label = ttk.Label(
            frame, text="Transmission Beam Location (x,y):"
        )
        trans_beam_location_label.grid(
            row=4, column=0, sticky="w", pady=10, padx=10)

        # Transmission beam location Error label
        trans_beam_location_error_label = ttk.Label(frame, foreground="tomato")
        trans_beam_location_error_label.grid(
            row=5, column=0, sticky="w", padx=10)

        t_beam_x_key = "transmission_beam_x"
        self._controller.register_validation(t_beam_x_key)

        # Transmission beam location X entry
        t_beam_location_x_entry = ttk.Entry(
            frame,
            width=3,
            textvariable=self._controller.transmission_beam_x,
            validate="focus",
            validatecommand=(
                frame.register(
                    WidgetUtils.show_error_message(
                        trans_beam_location_error_label,
                        t_beam_x_key,
                        self._controller.validate_tranmission_beam_location,
                    )
                ),
                "%d",
                "%P",
            ),
        )
        t_beam_location_x_entry.grid(row=4, column=1, sticky="e", pady=10)

        trans_beam_location_separator_label = ttk.Label(frame, text=",")
        trans_beam_location_separator_label.grid(
            row=4, column=2, sticky="e", pady=10, padx=10
        )

        t_beam_y_key = "transmission_beam_y"
        self._controller.register_validation(t_beam_y_key)

        # Transmission beam location Y entry
        t_beam_location_y_entry = ttk.Entry(
            frame,
            width=5,
            textvariable=self._controller.transmission_beam_y,
            validate="focus",
            validatecommand=(
                frame.register(
                    WidgetUtils.show_error_message(
                        trans_beam_location_error_label,
                        t_beam_y_key,
                        self._controller.validate_tranmission_beam_location,
                    )
                ),
                "%d",
                "%P",
            ),
        )
        t_beam_location_y_entry.grid(row=4, column=3, sticky="e", pady=10)
