"""Module for creating the ProcessFrame class used in the processing window."""

from tkinter import ttk

from gui.base import BaseFrame, BaseText


class ProcessFrame(BaseFrame):
    """A frame widget for displaying process logs."""

    def __init__(self, parent):
        """
        Initialize the ProcessFrame.

        Args:
            parent (tk.Widget): The parent widget to which this frame is attached.
        """
        super().__init__(parent)
        self.frame = ttk.Frame(parent)
        self.frame.grid(row=0, column=0, sticky="nsew")
        self.frame.rowconfigure(0, weight=1)
        self.frame.columnconfigure(0, weight=1)
        # Text field to enter keywords
        self.log_window = BaseText(self.frame)
        self.log_window.widget.config(wrap="word", width=25)
        self.log_window.widget.grid(
            row=0, column=0, sticky="nsew", padx=(10, 0), pady=10
        )

    def build(self):
        """
        Configure and add a vertical scrollbar to the text widget.
        """
        # Add scrollbar to Text field
        scrollbar = ttk.Scrollbar(self.frame, command=self.log_window.widget.yview)
        self.log_window.widget.config(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky="ns", pady=10)

    def get_widgets(self):
        """
        Get the widgets in the frame.

        Returns:
            list: A list of widgets contained in the frame.
        """
        return self.widgets
