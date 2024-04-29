from typing import Callable
from tkinter import ttk


class WidgetUtils:

    def show_error_message(
        error_label: ttk.Label,
        validation_key: str,
        validate: Callable[[str, str, Callable[[str], None]], None],
    ) -> Callable[[str], None]:

        def error(error_msg: str):
            if error_msg:
                error_label.config(text=error_msg)
            else:
                error_label.config(text="")

        return lambda action, value: validate(action, value, validation_key, error)

    def show_selected_file(selected_file_label: ttk.Label) -> Callable:
        def show(file_name: str):
            selected_file_label.config(text=f"Selected: {file_name}")

        return show

    def disable_on_invalidation(
        widget: ttk.Widget, all_validated: Callable[[None], bool]
    ):
        def callback(var: str, _, mode: str):
            is_valid = all_validated()
            disabled_state = "!disabled" if is_valid else "disabled"
            widget.state([disabled_state])

        return callback
