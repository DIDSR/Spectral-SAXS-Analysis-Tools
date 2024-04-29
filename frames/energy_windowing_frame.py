import tkinter as tk
from tkinter import ttk
from frames import BaseFrame, GlobalParametersFrame
from utils.theme import Icon, IconName
from utils import WidgetUtils
from controllers import EnergyWindowingController


class EnergyWindowingFrame(BaseFrame):

    def __init__(self, parent: tk.Tk):
        super().__init__(parent)
        self.global_params_frame = GlobalParametersFrame(self)
        self.parent = parent
        self.controller = EnergyWindowingController(
            self.parent, self.global_params_frame.controller)
        self.setup()

    def title(self) -> str:
        return "Energy Windowing Analysis"

    def setup(self) -> None:
        self.global_params_frame.grid(
            row=0, column=0, rowspan=2, pady=10, padx=10, sticky="ns")
        self.global_params_frame.anchor("center")
        self.frame_scan_data_section()
        self.frame_binning_section()
        self.show_example()

    def frame_scan_data_section(self):
        # Label frame
        scan_data_section = ttk.LabelFrame(self, text="Scan Data")
        scan_data_section.grid(row=0, column=1, sticky="ew",
                               ipadx=20, ipady=20, pady=10)
        scan_data_section.anchor("center")

        # Background file label
        bg_file_label = ttk.Label(scan_data_section, text="Background File:")
        bg_file_label.grid(row=0, column=0, sticky="w", pady=10, padx=10)

        # Background selected file label (only shows when a file was selected)
        bg_selected_file_label = ttk.Label(
            scan_data_section, text="", style="info.TLabel", foreground="dodgerBlue"
        )
        bg_selected_file_label.grid(row=1, column=0, sticky="w", padx=10)

        bg_file_key = "bg_file"
        self.controller.register_validation(bg_file_key)
        file_icon = Icon.load(IconName.FILE_SEARCH)

        # Background file picker button
        bg_file_picker = ttk.Button(
            scan_data_section,
            text="Browse Files",
            style="Accent.TButton",
            padding=[10, 5, 10, 5],
            image=file_icon,
            compound="left",
            command=(
                lambda: self.controller.browse_file(
                    self.controller.FileOption.BACKGROUND,
                    WidgetUtils.show_selected_file(bg_selected_file_label),
                    bg_file_key,
                )
            ),
        )
        bg_file_picker.image_ref = file_icon
        bg_file_picker.grid(row=0, column=1, sticky="e", pady=10, padx=10)

        # Sample file label
        sample_file_label = ttk.Label(scan_data_section, text="Sample File:")
        sample_file_label.grid(row=2, column=0, sticky="w", pady=10, padx=10)

        # Sample selected file label (only shows when a file was selected)
        sample_selected_file_label = ttk.Label(
            scan_data_section, text="", style="info.TLabel", foreground="dodgerBlue"
        )
        sample_selected_file_label.grid(row=3, column=0, sticky="w", padx=10)

        sample_file_key = "sample_file"
        self.controller.register_validation(sample_file_key)
        # Sample file picker button
        sample_file_picker = ttk.Button(
            scan_data_section,
            text="Browse Files",
            style="Accent.TButton",
            padding=[10, 5, 10, 5],
            image=file_icon,
            compound="left",
            command=(
                lambda: self.controller.browse_file(
                    self.controller.FileOption.SAMPLE,
                    WidgetUtils.show_selected_file(sample_selected_file_label),
                    sample_file_key,
                )
            ),
        )
        sample_file_picker.grid(row=2, column=1, sticky="e", pady=10, padx=10)

    def frame_binning_section(self):
        # Label frame
        binning_section = ttk.LabelFrame(self, text="Binning")
        binning_section.grid(row=1, column=1, sticky="ew",
                             ipadx=20, ipady=20, pady=20)
        binning_section.anchor("center")

        # Energy Range label
        energy_range_label = ttk.Label(
            binning_section, text="Energy Range (keV):")
        energy_range_label.grid(row=0, column=0, sticky="w", pady=10, padx=10)

        # Energy Range Error label
        energy_range_error_label = ttk.Label(
            binning_section, foreground="tomato")
        energy_range_error_label.grid(row=1, column=0, sticky="w", padx=10)

        energy_min_key = "energy_min"
        self.controller.register_validation(energy_min_key)
        # Energy Range Min spinbox
        energy_range_min_spinbox = ttk.Spinbox(
            binning_section,
            width=5,
            textvariable=self.controller.energy_range_min,
            validate="focus",
            validatecommand=(
                binning_section.register(
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

        energy_range_separator_label = ttk.Label(binning_section, text="-")
        energy_range_separator_label.grid(
            row=0, column=2, sticky="e", pady=10, padx=10)

        energy_max_key = "energy_max"
        self.controller.register_validation(energy_max_key)

        # Energy Range Max spinbox
        energy_range_max_spinbox = ttk.Spinbox(
            binning_section,
            width=5,
            textvariable=self.controller.energy_range_max,
            validate="focus",
            validatecommand=(
                binning_section.register(
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

        # Bin Width label
        bin_width_label = ttk.Label(binning_section, text="Bin Width (keV):")
        bin_width_label.grid(row=2, column=0, sticky="w", pady=10, padx=10)

        # Bin Width Error label
        bin_width_error_label = ttk.Label(binning_section, foreground="tomato")
        bin_width_error_label.grid(row=3, column=0, sticky="w", padx=10)

        bin_width_key = "bin_width"
        self.controller.register_validation(bin_width_key)

        # Bin Width entry
        bin_width_entry = ttk.Entry(
            binning_section,
            width=5,
            textvariable=self.controller.bin_width,
            validate="focus",
            validatecommand=(
                binning_section.register(
                    WidgetUtils.show_error_message(
                        bin_width_error_label,
                        bin_width_key,
                        self.controller.validate_bin_width,
                    )
                ),
                "%d",
                "%P",
            ),
        )
        bin_width_entry.grid(row=2, column=1, sticky="e", padx=10, pady=10)

        # Energy Window Width label
        energy_window_width_label = ttk.Label(
            binning_section, text="Energy Window Width (keV):"
        )
        energy_window_width_label.grid(
            row=4, column=0, sticky="w", pady=10, padx=10)

        # Energy Window Width Error label
        energy_window_width_error_label = ttk.Label(
            binning_section, foreground="tomato"
        )
        energy_window_width_error_label.grid(
            row=5, column=0, sticky="w", padx=10)

        energy_window_width_key = "energy_window_width"
        self.controller.register_validation(energy_window_width_key)

        # Energy Window Width entry
        energy_window_width_entry = ttk.Entry(
            binning_section,
            width=5,
            textvariable=self.controller.energy_window_width,
            validate="focus",
            validatecommand=(
                binning_section.register(
                    WidgetUtils.show_error_message(
                        energy_window_width_error_label,
                        energy_window_width_key,
                        self.controller.validate_energy_window_width,
                    )
                ),
                "%d",
                "%P",
            ),
        )
        energy_window_width_entry.grid(
            row=4, column=1, sticky="e", padx=10, pady=10)

        # Submit / Plot button
        plot_button = ttk.Button(
            binning_section,
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

    def show_example(self):
        # Example label
        example_label = ttk.Label(
            self,
            style="info.TLabel",
            foreground="dodgerBlue",
            text="Example: Energy Range: 30 - 45 keV; Bin Width: 1 keV; Energy Window Width: 5 keV",
        )
        example_label.grid(row=3, column=1, sticky="w", pady=10, padx=10)
