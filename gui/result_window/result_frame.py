"""Module for creating the ResultFrame class used in the result window."""

from tkinter import ttk

from gui.base import BaseFrame, BaseText


class ResultFrame(BaseFrame):
    """A frame widget for displaying clustering results."""

    def __init__(self, parent):
        """
        Initialize the ResultFrame.

        Args:
            parent (tk.Widget): The parent widget to which this frame is attached.
        """
        super().__init__(parent)
        self.frame = ttk.Frame(parent)
        self.frame.grid(row=0, column=0, sticky="nsew")
        self.frame.rowconfigure(0, weight=1)
        self.frame.columnconfigure(0, weight=1)
        # Text field to enter keywords
        self.result_window = BaseText(self.frame)
        self.result_window.widget.config(wrap="word", width=25)
        self.result_window.widget.grid(
            row=0, column=0, sticky="nsew", padx=(10, 0), pady=10
        )

    def build(self):
        """
        Configure and add a vertical scrollbar to the text widget.
        """
        # Add scrollbar to Text field
        scrollbar = ttk.Scrollbar(self.frame, command=self.result_window.widget.yview)
        self.result_window.widget.config(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky="ns", pady=10)

    def get_widgets(self):
        """
        Get the widgets in the frame.

        Returns:
            list: A list of widgets contained in the frame.
        """
        return self.widgets
