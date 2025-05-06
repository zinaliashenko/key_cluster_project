"""A module for creating ResultWindow class."""

import tkinter as tk

from gui.base import BaseWindow, WindowConfig
from gui.result_window.result_frame import ResultFrame


class ResultWindow(BaseWindow):
    """A class for creating resulting window."""

    def __init__(self, title, window_size, row_weight, column_weight, theme_file):
        """
        Window configuration parameters inherited from the BaseWindow base class.

        Args:
            title (str): The title text of the window.
            window_size (str): The size of the window in "WidthxHeight" format (e.g., "800x600").
            row_weight (int): Weight for row grid resizing. Default is 1.
            column_weight (int): Weight for column grid resizing. Default is 1.
            theme_file (str, optional): Path to a theme file for styling the window. Default is None.
        """
        config = WindowConfig(title, window_size, row_weight, column_weight, theme_file)
        super().__init__(config)
        self.result_frame = ResultFrame(self.window)

    def show(self):
        """
        Configures row and column grid weight for layout management,
        and displays widgets in the window.
        """
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)
        self.result_frame.build()

    def get_result_window(self):
        """
        Returns:
            An instance of a text field widget for displaying logs.
        """
        return self.result_frame.result_window.widget

    def update_result_window(self, controller):
        """Updates result window."""
        result_window = self.get_result_window()

        result_window.delete("1.0", tk.END)
        results = controller.print_result()

        for name, items in results.items():
            result_window.insert(tk.END, f"\n{name} ({len(items)} phrases):\n")
            for item in items:
                result_window.insert(tk.END, f"  - {item}\n")

        result_window.see(tk.END)
