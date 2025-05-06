"""
This module defines the LeftFrame class for the GUI, which allows users to
manually input keywords or upload them from a file.
"""

from tkinter import filedialog, ttk

from core.data_loader import LoadDataFromFile
from gui.base import BaseButton, BaseFrame, BaseText


class LeftFrame(BaseFrame):
    """
    GUI frame for the left side of the application window.

    Provides a text input area for entering keywords and a button to upload
    keywords from a file. Supports vertical scrolling for long text input.
    """

    def __init__(self, parent):
        """
        Initialize the LeftFrame.

        Args:
            parent (tk.Frame): The parent widget to attach this frame to.
        """
        super().__init__(parent)
        self.text = None
        self.frame = ttk.Frame(parent)
        self.frame.grid(row=1, column=0, sticky="nsew")
        self.frame.rowconfigure(0, weight=1)
        self.frame.rowconfigure(1, weight=0)
        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=0)

    def build(self):
        """
        Build the layout of the frame.

        Adds a text field with placeholder text, a vertical scrollbar,
        and a button to upload keywords from a file.
        """
        # Text field to enter keywords
        placeholder = "Enter \nyour keywords \nfor clustering \nhere..."
        self.text = BaseText(self.frame, placeholder)
        self.text.widget.config(wrap="word", width=25)
        self.text.widget.grid(row=0, column=0, sticky="nsew", padx=(10, 0), pady=10)

        # Add scrollbar to Text field
        scrollbar = ttk.Scrollbar(self.frame, command=self.text.widget.yview)
        self.text.widget.config(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky="ns", pady=10)

        # Load button
        btn_cluster = BaseButton(
            self.frame,
            text="Download file",
            command=lambda: self.load_file(),
        )
        btn_cluster.widget.config(width=20)
        btn_cluster.widget.grid(row=1, column=0, pady=(20, 10), padx=40, sticky="s")

    def load_file(self):
        """
        Open a file dialog to select a file and load keywords from it.

        Loads the content and inserts it into the text input field.
        """
        file_path = filedialog.askopenfilename(
            title="Виберіть файл",
            filetypes=(
                ("Text files", "*.txt"),
                ("Text files", "*.csv"),
                ("All files", "*.*"),
            ),
        )
        if file_path:
            print("You picked up:", file_path)
        if file_path:
            loader = LoadDataFromFile(file_path)
            loader.load()
            content = loader.to_list()
            content = "\n".join(content) + "\n"
            self.text.put_text_from_file(content)

    def get_widgets(self):
        """Return a dictionary of widgets in the frame."""
        return self.widgets
