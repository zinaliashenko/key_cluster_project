"""A module for creating ProcessWindow class."""

import queue
import tkinter as tk

from gui.base import BaseWindow, WindowConfig
from gui.process_window.process_frame import ProcessFrame


class ProcessWindow(BaseWindow):
    """A class for creating processing window."""

    def __init__(self, title, window_size, row_weight, column_weight, theme_file):
        """
        Window configuration parameters inherited from the BaseWindow base class.

        Args:
            title (str): The title text of the window.
            window_size (str): The size of the window in "WidthxHeight" format.
            row_weight (int): Weight for row grid resizing. Default is 1.
            column_weight (int): Weight for column grid resizing. Default is 1.
            theme_file (str): Path to a theme file for styling the window. Default is None.
        """
        config = WindowConfig(title, window_size, row_weight, column_weight, theme_file)
        super().__init__(config)
        self.process_frame = ProcessFrame(self.window)

    def show(self):
        """
        Configures row and column grid weight for layout management,
        and displays widgets in the window.
        """
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)
        self.process_frame.build()

    def get_log_window(self):
        """
        Returns:
            An instance of a text field widget for displaying logs.
        """
        return self.process_frame.log_window.widget

    def update_log_window(self, controller):
        """Updates log window in recursion mode."""
        log_window = self.get_log_window()  # get log window at every call
        try:
            while True:
                # takes messages from queue if any
                message = controller.log_queue.get_nowait()
                log_window.insert(tk.END, message + "\n\n")
                log_window.see(tk.END)  # autoscroll
        except queue.Empty:
            pass
        log_window.after(100, self.update_log_window, controller)  # recursion
