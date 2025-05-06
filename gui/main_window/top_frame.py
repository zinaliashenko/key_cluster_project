"""
This module defines the TopFrame class, which represents the top section of the GUI.
It contains the main title and a subtitle to guide the user.
"""

from tkinter import ttk

from gui.base import BaseFrame


class TopFrame(BaseFrame):
    """
    TopFrame class defines the top portion of the GUI.
    It includes a main title and a subtitle that provide context to the user.
    """

    def __init__(self, parent):
        """
        Initialize the TopFrame.

        Args:
            parent: The parent tkinter widget to attach this frame to.
        """
        super().__init__(parent)
        self.frame.grid(row=0, column=0, columnspan=3, sticky="n")
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=1)
        self.frame.rowconfigure(1, weight=1)

    def build(self):
        """
        Build the widgets in the TopFrame.

        Creates a main title and a subtitle, and places them using grid geometry.
        Stores the widgets in self.widgets for later access.
        """
        # Main title
        lbl_name = ttk.Label(
            self.frame,
            text="Are you ready to CLUSTER your KEYWORDS??",
            font=("Arial", 16, "bold"),
        )
        lbl_name.grid(row=0, column=0, sticky="we", pady=(10, 5))

        # Subtitle
        lbl_subname = ttk.Label(
            self.frame,
            text="to start working, please paste the key words in the left text field...",
            font=("Arial", 10),
        )
        lbl_subname.grid(row=1, column=0, sticky="w", padx=(10), pady=(10, 5))

        self.widgets["lbl_name"] = lbl_name
        self.widgets["lbl_subname"] = lbl_subname

    def get_widgets(self):
        """Return a dictionary of widgets in the frame."""
        return self.widgets
