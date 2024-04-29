import tkinter as tk
from tkinter import ttk
from frames import BaseFrame, GlobalParametersFrame
from utils.theme import Icon, IconName
from utils import WidgetUtils
from controllers import ScanReconstructionController
"""
Handles all of the visual elements for the scan reconstruction tab
"""


class ScanReconstructionFrame(BaseFrame):

    def __init__(self, parent: tk.Tk):
        super().__init__(parent)
        self.global_params_frame = GlobalParametersFrame(self)
        self.parent = parent
        self.controller = ScanReconstructionController(
            self.parent, self.global_params_frame.controller)
        self.setup()

    def title(self) -> str:
        return "Raster Scan Reconstruction"

    def setup(self) -> None:
        self.global_params_frame.grid(
            row=0, column=0, rowspan=2, sticky="ns", pady=10, padx=10)
        self.global_params_frame.anchor("center")
        scan_data_frame = self.setup_scan_data_frame()
        self.setup_file_pickers(scan_data_frame)

        params_frame = self.setup_params_frame()
        self.setup_energy_range(params_frame)
        self.setup_integral_q_range(params_frame)
        self.setup_scan_width(params_frame)
        self.setup_submit(params_frame)

    def setup_scan_data_frame(self):

        # Label frame
        scan_data_section = ttk.LabelFrame(self, text="Scan Data")
        scan_data_section.grid(row=0, column=1, sticky="ew",
                               ipadx=20, ipady=20, pady=10)
        scan_data_section.anchor("center")
        return scan_data_section

    def setup_file_pickers(self, frame: tk.LabelFrame):

        # Background file label
        bg_file_label = ttk.Label(frame, text="Background File:")
        bg_file_label.grid(row=0, column=0, sticky="w", pady=10, padx=10)

        # Background selected file label (only shows when a file was selected)
        bg_selected_file_label = ttk.Label(
            frame, text="", style="info.TLabel", foreground="dodgerBlue"
        )
        bg_selected_file_label.grid(row=1, column=0, sticky="w", padx=10)
        bg_file_key = "bg_file"
        self.controller.register_validation(bg_file_key)

        file_icon = Icon.load(IconName.FILE_SEARCH)
        # Background file picker button
        bg_file_picker = ttk.Button(
            frame,
            text="Browse Files",
            style="Accent.TButton",
            padding=[10, 5, 10, 5],
            image=file_icon,
            compound="left",
            width=15,
            command=(
                lambda: self.controller.browse_bg_file(
                    WidgetUtils.show_selected_file(
                        bg_selected_file_label), bg_file_key
                )
            ),
        )
        # without this line, the image won't show. Only needs to be done once for an image reference see: https://stackoverflow.com/questions/41863330/issue-with-button-images-in-ttk-python
        bg_file_picker.image_ref = file_icon
        bg_file_picker.grid(row=0, column=1, sticky="e", pady=10, padx=10)

        # Sample file label
        sample_file_label = ttk.Label(frame, text="Sample File(s):")
        sample_file_label.grid(row=2, column=0, sticky="w", pady=10, padx=10)

        # Sample selected file label (only shows when a file was selected)
        sample_selected_file_label = ttk.Label(
            frame, text="", style="info.TLabel", foreground="dodgerBlue"
        )
        sample_selected_file_label.grid(row=3, column=0, sticky="w", padx=10)

        sample_directory_key = "sample_directory"
        self.controller.register_validation(sample_directory_key)

        folder_icon = Icon.load(IconName.FOLDER_SEARCH)
        # Sample file picker button
        sample_file_picker = ttk.Button(
            frame,
            text="Browse Directory",
            style="Accent.TButton",
            padding=[10, 5, 10, 5],
            image=folder_icon,
            compound="left",
            width=15,
            command=(
                lambda: self.controller.browse_sample_directory(
                    WidgetUtils.show_selected_file(sample_selected_file_label),
                    sample_directory_key,
                )
            ),
        )
        # without this line, the image won't show. Only needs to be done once for an image reference see: https://stackoverflow.com/questions/41863330/issue-with-button-images-in-ttk-python
        sample_file_picker.image_ref = folder_icon
        sample_file_picker.grid(row=2, column=1, sticky="e", pady=10, padx=10)

        # Sample file extension chooser combobox
        file_extension_combobox = ttk.Combobox(
            frame,
            textvariable=self.controller.file_extension,
            width=4,
            state="normal",  # so that the combobox is editable
        )
        file_extension_combobox.config(
            values=self.controller.file_extension_options)
        file_extension_combobox.grid(
            row=3, column=1, sticky="e", pady=10, padx=10)

    def setup_params_frame(self):
        # Label frame
        params_section = ttk.LabelFrame(self, text="Analysis")
        params_section.grid(row=1, column=1, sticky="ew",
                            ipadx=20, ipady=20, pady=20)
        params_section.anchor("center")
        return params_section

    def setup_energy_range(self, frame: tk.LabelFrame):
        # Energy Range label
        energy_range_label = ttk.Label(frame, text="Energy Range (keV):")
        energy_range_label.grid(row=0, column=0, sticky="w", pady=10, padx=10)

        # Energy Range Error label
        energy_range_error_label = ttk.Label(frame, foreground="tomato")
        energy_range_error_label.grid(row=1, column=0, sticky="w", padx=10)

        energy_min_key = "energy_min"
        self.controller.register_validation(energy_min_key)
        # Energy Range Min spinbox
        energy_range_min_spinbox = ttk.Spinbox(
            frame,
            width=3,
            textvariable=self.controller.energy_range_min,
            validate="focus",
            validatecommand=(
                frame.register(
                    WidgetUtils.show_error_message(
                        energy_range_error_label,
                        energy_min_key,
                        self.controller.validate_energy_min,
                    )
                ),
                "%d",
                "%P",
            ),
            from_=self.controller.ENERGY_RANGE_MIN,
            to=self.controller.ENERGY_RANGE_MAX,
        )
        energy_range_min_spinbox.grid(row=0, column=1, sticky="e", pady=10)

        energy_range_separator_label = ttk.Label(frame, text="-")
        energy_range_separator_label.grid(
            row=0, column=2, sticky="e", pady=10, padx=10)

        energy_max_key = "energy_max"
        self.controller.register_validation(energy_max_key)

        # Energy Range Max spinbox
        energy_range_max_spinbox = ttk.Spinbox(
            frame,
            width=3,
            textvariable=self.controller.energy_range_max,
            validate="focus",
            validatecommand=(
                frame.register(
                    WidgetUtils.show_error_message(
                        energy_range_error_label,
                        energy_max_key,
                        self.controller.validate_energy_max,
                    )
                ),
                "%d",
                "%P",
            ),
            from_=self.controller.ENERGY_RANGE_MIN,
            to=self.controller.ENERGY_RANGE_MAX,
        )
        energy_range_max_spinbox.grid(row=0, column=3, sticky="e", pady=10)

    def setup_integral_q_range(self, frame: tk.LabelFrame):
        # Integral q Range label
        integral_q_range_label = ttk.Label(
            frame, text="Integral q Range (nm\u207b\u00B9)"
        )
        integral_q_range_label.grid(
            row=2, column=0, sticky="w", pady=10, padx=10)

        # Integral q Range Error label
        integral_q_range_error_label = ttk.Label(frame, foreground="tomato")
        integral_q_range_error_label.grid(row=3, column=0, sticky="w", padx=10)

        integral_q_start_key = "integral_q_start"
        self.controller.register_validation(integral_q_start_key)

        # Integral q Range Start entry
        integral_q_range_start_entry = ttk.Entry(
            frame,
            width=5,
            textvariable=self.controller.integral_q_start,
            validate="focus",
            validatecommand=(
                frame.register(
                    WidgetUtils.show_error_message(
                        integral_q_range_error_label,
                        integral_q_start_key,
                        self.controller.validate_q_start,
                    )
                ),
                "%d",
                "%P",
            ),
        )
        integral_q_range_start_entry.grid(row=2, column=1, sticky="e", pady=10)

        integral_q_range_separator_label = ttk.Label(frame, text="to")
        integral_q_range_separator_label.grid(
            row=2, column=2, sticky="e", pady=10, padx=10
        )

        integral_q_end_key = "integral_q_end"
        self.controller.register_validation(integral_q_end_key)
        # Integral q Range End Entry
        integral_q_range_end_entry = ttk.Entry(
            frame,
            width=5,
            textvariable=self.controller.integral_q_end,
            validate="focus",
            validatecommand=(
                frame.register(
                    WidgetUtils.show_error_message(
                        integral_q_range_error_label,
                        integral_q_end_key,
                        self.controller.validate_q_end,
                    )
                ),
                "%d",
                "%P",
            ),
        )
        integral_q_range_end_entry.grid(row=2, column=3, sticky="e", pady=10)

    def setup_scan_width(self, frame: tk.LabelFrame):
        # Scan width label
        scan_width_label = ttk.Label(frame, text="Scan Width")
        scan_width_label.grid(row=4, column=0, sticky="w", pady=10, padx=10)

        # Scan width Error label
        scan_width_error_label = ttk.Label(frame, foreground="tomato")
        scan_width_error_label.grid(row=5, column=0, sticky="w", padx=10)

        scan_width_key = "scan_width"
        self.controller.register_validation(scan_width_key)

        # Scan width entry
        scan_width_entry = ttk.Entry(
            frame,
            width=5,
            textvariable=self.controller.scan_width,
            validate="focus",
            validatecommand=(
                frame.register(
                    WidgetUtils.show_error_message(
                        scan_width_error_label,
                        scan_width_key,
                        self.controller.validate_scan_width,
                    )
                ),
                "%d",
                "%P",
            ),
        )
        scan_width_entry.grid(row=4, column=1, sticky="e", pady=10)

    def setup_submit(self, frame: tk.LabelFrame):
        # Submit / Plot button
        plot_button = ttk.Button(
            frame,
            text="Generate Plot",
            style="Accent.TButton",
            padding=[10, 5, 10, 5],
            command=self.controller.submit,
        )
        button_disable_state = (
            "!disabled" if self.controller.are_all_valid else "disabled"
        )
        plot_button.state(
            [button_disable_state]
        )  # Call the first time to validate default inputs
        plot_button.grid(row=6, column=0, columnspan=4,
                         sticky="ew", pady=10, padx=10)

        self.controller.register_submit_validation_refresh(
            WidgetUtils.disable_on_invalidation(
                plot_button, self.controller.are_all_valid
            )
        )
